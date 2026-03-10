import json
from datetime import datetime, timedelta, timezone
from src.redis_client import redis_client
from src.config import get_config
import redis
from sqlalchemy.ext.asyncio import AsyncSession

conf = get_config()

TIMEZONE_OFFSET = -5  # hours
TIMEZONE = timezone(timedelta(hours=TIMEZONE_OFFSET))

async def call_to_max(house_id: int, flat: int, session: AsyncSession):    
    print('')

    
def update_intercom_data(
    tech_name: str,
    battery_level: int | None = None,
    battery_temp: float | None = None
) -> dict | bool:
    """
    Обновляет информацию о домофоне в Redis.
    Если домофон новый — добавляет его.
    Если домофон существует — обновляет last_update и параметры батареи.
    
    Возвращает:
        dict — обновлённый объект домофона
        False — при неудаче
    """
    max_retries = 5

    for attempt in range(max_retries):
        with redis_client.pipeline() as pipe:
            try:
                pipe.watch(conf.redis.INTERCOMS_KEY)

                intercoms_json = pipe.get(conf.redis.INTERCOMS_KEY)
                current_intercoms = json.loads(intercoms_json) if intercoms_json else []

                current_time_utc = datetime.now(timezone.utc)
                current_time = current_time_utc.astimezone(TIMEZONE) 
                current_time_iso = current_time.isoformat()

                found = False
                updated_intercom = None

                for intercom in current_intercoms:
                    if intercom.get('tech_name') == tech_name:
                        intercom['last_update'] = current_time_iso
                        if battery_level is not None:
                            intercom['battery_level'] = battery_level
                        if battery_temp is not None:
                            intercom['battery_temp'] = battery_temp
                        updated_intercom = intercom
                        found = True
                        break

                if not found:
                    updated_intercom = {
                        'tech_name': tech_name,
                        'last_update': current_time_iso,
                        'date_start': current_time_iso,
                        'battery_level': battery_level,
                        'battery_temp': battery_temp
                    }
                    current_intercoms.append(updated_intercom)
                    # print(f"[{current_time.strftime('%H:%M:%S')}] Домофон с tech_name={tech_name} добавлен.")
                # else:
                #     print(f"[{current_time.strftime('%H:%M:%S')}] Домофон с tech_name={tech_name} обновлен.")

                pipe.multi()
                pipe.set(conf.redis.INTERCOMS_KEY, json.dumps(current_intercoms))
                pipe.execute()

                print(f"[{current_time.strftime('%H:%M:%S')}] Данные для tech_name={tech_name} успешно записаны в Redis.")
                return updated_intercom  # Возвращаем обновлённый объект

            except redis.WatchError:
                print(f"[{current_time.strftime('%H:%M:%S')}] WatchError: Ключ '{conf.redis.INTERCOMS_KEY}' изменен другим клиентом. Попытка {attempt + 1}/{max_retries}...")
            except Exception as e:
                print(f"[{current_time.strftime('%H:%M:%S')}] Произошла ошибка: {e}")
                pipe.unwatch()
                return False

    print(f"[{current_time.strftime('%H:%M:%S')}] Не удалось обновить данные для tech_name={tech_name} после {max_retries} попыток.")
    return False

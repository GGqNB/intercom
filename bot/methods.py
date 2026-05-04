from request import give_device
from config import ADMIN_CHAT_ID
from keyboards import HOUSE_MAP, main_menu_kb
from datetime import datetime, timedelta
from typing import Optional


def format_date(iso_date_string: str) -> str:
    try:
        if 'T' in iso_date_string:
            iso_date_string = iso_date_string.split('.')[0].replace('T', ' ')
        else:
            iso_date_string = iso_date_string[:19]

        dt = datetime.strptime(iso_date_string, "%Y-%m-%d %H:%M:%S")
        
        dt += timedelta(hours=5)

        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_date_string


def time_ago(iso_date_string: str) -> str:
    if not iso_date_string:
        return ''
    
    try:
        clean_date = iso_date_string.split('.')[0].replace('T', ' ')
        device_time = datetime.strptime(clean_date[:19], "%Y-%m-%d %H:%M:%S")
        
        # 👇 КОСТЫЛЬ: компенсируем -5 часов
        device_time += timedelta(hours=5)
        
        now = datetime.now()
        
        diff_seconds = int((now - device_time).total_seconds())
        
        if diff_seconds < 0:
            return "в будущем"
        elif diff_seconds < 60:
            return f"{diff_seconds} секунд назад"
        elif diff_seconds < 3600:
            minutes = diff_seconds // 60
            return f"{minutes} минут назад"
        elif diff_seconds < 86400:
            hours = diff_seconds // 3600
            return f"{hours} часов назад"
        else:
            days = diff_seconds // 86400
            return f"{days} дней назад"
    
    except Exception as e:
        print(f"Ошибка time_ago: {e}")
        return ""


def format_device_message(redis_data: dict) -> str:
    if not redis_data or redis_data.get('status') != 'success':
        return "❌ Не удалось получить данные с устройства"
    
    devices = redis_data.get('data', [])
    
    if not devices:
        return "📭 Нет доступных устройств"
    
    device_count = len(devices)
    device_word = get_device_word(device_count)
    message_parts = [f"📱 *Информация об устройствах* ({device_count} {device_word})\n"]
    
    for idx, device in enumerate(devices, 1):
        tech_name = device.get('tech_name', 'Неизвестно')
        battery_level = device.get('battery_level', 'Нет данных')
        battery_temp = device.get('battery_temp', 'Нет данных')
        
        last_update_raw = device.get('last_update', '')
        date_start_raw = device.get('date_start', '')
        
        last_update_formatted = format_date(last_update_raw)
        last_update_ago = time_ago(last_update_raw)
        
        date_start_formatted = format_date(date_start_raw)
        date_start_ago = time_ago(date_start_raw)
        
        message_parts.append(f"*Устройство {idx}/{device_count}*")
        message_parts.append(f"🔧 `{tech_name}`")
        
        battery_icon = "🔋"
        if isinstance(battery_level, (int, float)):
            if battery_level <= 15:
                battery_icon = "🪫"
            elif battery_level <= 30:
                battery_icon = "⚠️"
        
        temp_icon = "🌡️"
        if isinstance(battery_temp, (int, float)):
            if battery_temp > 45:
                temp_icon = "🔥"
            elif battery_temp > 35:
                temp_icon = "⚠️"
        
        message_parts.append(f"{battery_icon} Батарея: {battery_level}%")
        message_parts.append(f"{temp_icon} Температура: {battery_temp}°C")
        message_parts.append(f"🕐 Последнее обновление: {last_update_formatted} ({last_update_ago})")
        message_parts.append(f"📅 Начало работы: {date_start_formatted} ({date_start_ago})")
        
        intercom = device.get('intercom')
        if intercom and isinstance(intercom, dict):
            intercom_name = intercom.get('name', 'Неизвестно')
            intercom_tech = intercom.get('tech_name', 'Неизвестно')
            entry_name = intercom.get('entry', {}).get('name', 'Неизвестно')
            
            message_parts.append(f"\n🏢 Домофон: {intercom_name}")
            message_parts.append(f"🔧 Тех. название: `{intercom_tech}`")
            message_parts.append(f"🚪 Точка входа: {entry_name}")
            
            house_id = intercom.get('entry', {}).get('house_id')
            if house_id:
                house_text = None
                for house_info in HOUSE_MAP.values():
                    if house_info.get('id') == house_id:
                        house_text = house_info.get('text')
                        break
                
                if house_text:
                    message_parts.append(f"🏠 Дом: {house_text}")
                else:
                    message_parts.append(f"🏠 ID дома: {house_id}")
            else:
                message_parts.append("🏠 Дом: не указан")
        else:
            message_parts.append("\n📵 Домофон: не подключен")
        
        if idx < device_count:
            message_parts.append("\n" + "─" * 40 + "\n")
    
    return "\n".join(message_parts)


def get_device_word(count: int) -> str:
    if count % 10 == 1 and count % 100 != 11:
        return "устройство"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return "устройства"
    else:
        return "устройств"
from src.config import get_config
import json
from src.redis_client import redis_client
from src.crm.intercom.models import Intercom
from typing import Any, Dict
import secrets
conf = get_config()

def get_logs_intercoms():
    intercoms_json = redis_client.get(conf.redis.INTERCOMS_KEY)
    return json.loads(intercoms_json) if intercoms_json else []

def intercom_to_dict(ic: Intercom) -> Dict[str, Any]:
                return {
                    "id": ic.id,
                    "name": ic.name,
                    "tech_name": ic.tech_name,
                    "entry_id": ic.entry_id,
                    "entry": {
                        "id": ic.entry.id,
                        "name": ic.entry.name,
                        "flat_first": ic.entry.flat_first,
                        "flat_last": ic.entry.flat_last,
                        "house_id": ic.entry.house_id,
                    } if getattr(ic, "entry", None) else None,
                }


def generate_token() -> str:
    return secrets.token_urlsafe(32)


async def create_action_token(data: Dict[str, Any]) -> str:
    token = generate_token()
    key = f"{conf.redis.MAX_TOKEN_PREFIX}:{token}"

    redis_client.set(
        key,
        json.dumps(data),
        ex=conf.redis.MAX_TOKEN_TTL
    )

    return token
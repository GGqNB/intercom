import redis
from src.config import get_config

conf = get_config()

redis_client = redis.from_url(
    conf.redis.url,
    decode_responses=True
)
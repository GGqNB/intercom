import requests

from src.config import get_config
from src.crm.helper.stown import get_access_token
from src.redis_client import redis_client

conf = get_config()

async def flat_by_phone(phone):
    try:
        token = redis_client.get(conf.redis.STOWN_KEY)
        if not token:
            token = get_access_token()

        headers = {'Authorization': f'JWT {token}'}
        url = conf.stown.FLAT_BY_NUBMER_URL.format(phone=phone)
        print(url)
        api_response = requests.post(
            url,
            headers=headers
            )
        print(api_response)
        if api_response.status_code != 200:
            raise Exception("Stown API error: " + api_response.text)

        data = api_response.json()

        return {
            "status": data,
        }

    except Exception as e:
        return {"error": str(e)}
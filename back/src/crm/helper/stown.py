import requests
from src.redis_client import redis_client
from src.config import get_config

conf = get_config()

def get_access_token():

    try:
        data ={
        "username": f"{conf.stown.LOGIN}",
        "password": f"{conf.stown.PASSWORD}"
        }
        response = requests.post(conf.stown.AUTH_URL, data=data)
        print(response)
        response.raise_for_status() 
        token_data = response.json()
        redis_client.set(conf.redis.STOWN_KEY, token_data.get('token'))
        return redis_client.get(conf.redis.STOWN_KEY)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе токена: {e}")
        return None

# def get_access_token_intercom():

#     try:
#         data ={
#         "username": f"{conf.stown.LOGIN}",
#         "password": f"{conf.stown.PASSWORD}"
#         }
#         response = requests.post(conf.stown.AUTH_URL, data=data)
#         print(response)
#         response.raise_for_status() 
#         token_data = response.json()
#         redis_client.set(conf.redis.STOWN_KEY, token_data.get('token'))
#         return redis_client.get(conf.redis.STOWN_KEY)
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе токена: {e}")
#         return None
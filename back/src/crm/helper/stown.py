import requests
from src.redis_client import redis_client
from src.config import get_config

conf = get_config()

def get_access_token():

    data = conf.stown.build_login_data
    try:
        data2 ={
        "username": "9088997616",
        "password": "1234567890"
        }
        response = requests.post(conf.stown.AUTH_URL, data=data2)
        print(response)
        response.raise_for_status() 
        token_data = response.json()
        redis_client.set(conf.redis.STOWN_KEY, token_data.get('token'))
        return redis_client.get(conf.redis.STOWN_KEY)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе токена: {e}")
        return None

def open_local_lock(lock_id: int, code: str, local_url_base: str):
    data = conf.stown_local.build_login_data
    auth_url = f'http://{local_url_base}{conf.stown_local.AUTH_URL}'
    print(auth_url)

    try:
        login_response = requests.post(auth_url, data=data, timeout=3)
        login_response.raise_for_status()
        token_data = login_response.json()
        access_token = token_data.get("access_token")
    except requests.exceptions.Timeout:
        print("Ошибка: сервер не ответил вовремя (таймаут авторизации)")
        return 'error_timeout'
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при авторизации: {e}")
        return 'error'
    
    if not access_token:
        return {"error": "Не удалось получить токен"}

    # открытие
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        lock_url = f'http://{local_url_base}{conf.stown_local.OPEN_URL}/{lock_id}/{code}'
        lock_response = requests.get(lock_url, headers=headers, timeout=3)
        lock_response.raise_for_status()
        return lock_response.json()
    except requests.exceptions.Timeout:
        print("Ошибка: сервер не ответил вовремя (таймаут открытия)")
        return 'error_timeout'
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при открытии: {e}")
        return str(e)
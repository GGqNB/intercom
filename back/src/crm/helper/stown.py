import requests
from src.redis_client import redis_client
from src.config import TOKEN_KEY

def get_access_token(login, password, client_id, client_secret, token_url, scope=None):
    
    data = {
        'grant_type': 'password',
        'username': login,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    if scope:
        data['scope'] = scope

    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status() 
        token_data = response.json()
        redis_client.set(TOKEN_KEY, token_data.get('token'))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе токена: {e}")
        return None

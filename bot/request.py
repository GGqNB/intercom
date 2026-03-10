import aiohttp
from config import BACKEND_URL, API_KEY
import asyncio

async def register_user(payload: dict) -> bool:
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }

    timeout = aiohttp.ClientTimeout(total=5)  # максимум 5 секунд

    try:
        print('запрос')
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{BACKEND_URL}/api/users",
                json=payload,
                headers=headers
            ) as response:
                print(f"{BACKEND_URL}/api/users")
                print(f"{API_KEY}")
                if response.status == 201:
                    return {"success": True}
                if response.status == 418:
                    data = await response.json()
                    return {"success": False, "error": data.get("detail")}
                
                return {"success": False, "error": "server_error"}

    except asyncio.TimeoutError:
        print("Backend timeout")
        return {"success": False, "error": "server_timeout"}

    except Exception as e:
        print(f"Backend error: {e}")
        return {"success": False, f"error": {e}}
    
import aiohttp
from config import BACKEND_URL, API_KEY

async def get_user_settings(max_id: str) -> dict | None:
    """
    Запрос к backend для получения настроек пользователя по max_id.
    Возвращает словарь с данными пользователя или None, если не найдено.
    """

    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BACKEND_URL}/api/users/{max_id}",
                headers=headers,
                timeout=10
            ) as resp:

                if resp.status == 404:
                    return None

                if resp.status != 200:
                    return None
                data = await resp.json()
                print(data)
                return data

    except Exception as e:
        print(f"Ошибка запроса к backend: {e}")
        return None
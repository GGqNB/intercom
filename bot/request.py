import json

import aiohttp
from config import BACKEND_URL, API_KEY 
import asyncio

async def flat_by_number(phone: str, data) -> dict | None:

    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/api/users/max/{phone}",
                headers=headers,
                json=data,
                timeout=2
            ) as resp:

                print("STATUS:", resp.status)

                if resp.status == 404:
                    print("404")
                    return None

                if resp.status not in (200, 201):
                    print("ERROR:", resp.status)
                    return None

                # ✅ ВОТ ГЛАВНОЕ
                response_data = await resp.json()

                # 👀 красиво смотрим что пришло
                print(json.dumps(response_data, indent=2, ensure_ascii=False))

                return response_data

    except Exception as e:
        print(f"Ошибка запроса к backend: {e}")
        return None

# async def register_user(payload: dict) -> bool:
#     headers = {
#         "Authorization": f"{API_KEY}",
#         "Content-Type": "application/json"
#     }

#     timeout = aiohttp.ClientTimeout(total=5)  # максимум 5 секунд

#     try:
#         async with aiohttp.ClientSession(timeout=timeout) as session:
#             async with session.post(
#                 f"{BACKEND_URL}/api/users",
#                 json=payload,
#                 headers=headers
#             ) as response:
#                 print(f"{BACKEND_URL}/api/users")
#                 print(f"{API_KEY}")
#                 if response.status == 201:
#                     return {"success": True}
#                 if response.status == 418:
#                     data = await response.json()
#                     return {"success": False, "error": data.get("detail")}
                
#                 return {"success": False, "error": "server_error"}

#     except asyncio.TimeoutError:
#         print("Backend timeout")
#         return {"success": False, "error": "server_timeout"}

#     except Exception as e:
#         print(f"Backend error: {e}")
#         return {"success": False, f"error": {e}}
    

async def get_user_settings(max_id: str) -> dict | None:

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

                print(json.dumps(data))
                return data

    except Exception as e:
        print(f"Ошибка запроса к backend: {e}")
        return None

async def call_open_door_backend(open_token: str) -> dict:

    url = f"{BACKEND_URL}/open"
    headers = {"Authorization": f"{API_KEY}"}
    data = {"redis_open_token": open_token}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Ошибка backend: {resp.status} {text}")
            return await resp.json()

async def call_open_door_backend(open_token: str) -> dict:
    url = f"{BACKEND_URL}/api/open?redis_open_token={open_token}"
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as resp:
            try:
                resp_json = await resp.json()
            except Exception:
                resp_text = await resp.text()
                raise Exception(f"Некорректный ответ backend: {resp.status} {resp_text}")

            if resp.status == 200:
                return {"success": True, "data": resp_json}
            elif resp.status == 400:
                return {"success": False, "error": "❌ Токен недействителен или истёк"}
            elif resp.status >= 500:
                return {"success": False, "error": "❌ Ошибка сервера, попробуйте позже"}
            else:
                return {"success": False, "error": f"❌ Неизвестная ошибка: {resp_json}"}
            

async def give_device():
    url = f"{BACKEND_URL}/logs/redis-intercom"
    headers = {"Authorization": f"{API_KEY}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Ошибка backend: {resp.status} {text}")
            return await resp.json()
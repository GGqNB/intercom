import aiohttp
from config import BACKEND_URL, API_KEY


async def register_user(payload: dict) -> bool:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BACKEND_URL}/api/users",
                json=payload,
                headers=headers,
                timeout=10
            ) as response:

                if response.status == 200:
                    return True

                return False

    except Exception as e:
        print(f"Backend error: {e}")
        return False
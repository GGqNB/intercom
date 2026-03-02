from typing import Type, Dict, Any, List

from faker import Faker
from fastapi import Depends
from pydantic import BaseModel

from requests import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from src.crm.build.models import Entry, House
from src.crm.intercom.models import Intercom
from src.crm.location.models import City
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from fastapi import APIRouter
from fastapi.security.api_key import APIKey
from src.auth import get_api_key
import random
import string

def generate_fake_data(model_class: Type[BaseModel]) -> Dict[str, Any]:
    """
    Генерирует фейковые данные для Pydantic модели.  Теперь работает с учетом SQLAlchemy моделей.

    Args:
        model_class: Класс Pydantic модели.

    Returns:
        Словарь с фейковыми данными, соответствующими полям модели.
    """
    fields = model_class.model_fields
    data = {}
    for field_name, field in fields.items():
        field_type = field.type
        if field_name == "id":
            data[field_name] = Faker.pyint()  # Или другой подходящий генератор для ID
        elif field_type == str:
            data[field_name] = Faker.city()  # Или другой подходящий генератор для строк
        elif field_type == int:
            data[field_name] = Faker.pyint()
        elif field_type == float:
            data[field_name] = Faker.pyfloat()
        elif field_type == bool:
            data[field_name] = Faker.pybool()
        # Добавьте больше условий для других типов данных, которые вы используете
        else:
            data[field_name] = None  # Или другой дефолтный генератор

    return data


def generate_fake_instance(model_class: Type[BaseModel]) -> BaseModel:
    """
    Генерирует экземпляр Pydantic модели с фейковыми данными.

    Args:
        model_class: Класс Pydantic модели.

    Returns:
        Экземпляр Pydantic модели, заполненный фейковыми данными.
    """
    data = generate_fake_data(model_class)
    return model_class(**data)


def generate_fake_list(model_class: Type[BaseModel], count: int) -> List[BaseModel]:
    """
    Генерирует список экземпляров Pydantic моделей с фейковыми данными.

    Args:
        model_class: Класс Pydantic модели.
        count: Количество экземпляров для генерации.

    Returns:
        Список Pydantic моделей, заполненных фейковыми данными.
    """
    return [generate_fake_instance(model_class) for _ in range(count)]

router_fake = APIRouter(
    prefix="/fake",
    tags=["Работа с домофоном"]
)

def gen_tech_name() -> str:
    """Генерирует tech_name в формате xxx-xxx-xxx-xxx"""
    return "-".join(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
        for _ in range(4)
    )
#надо будет проверить
@router_fake.post("/seed")
async def seed_data(
    session: AsyncSession = Depends(get_async_session),
    api_key=Depends(get_api_key)
):
    city = City(id=1, name="Ханты-Мансийск")
    session.add(city)

    house1 = House(
        id=13,
        name="Объездная 57а",
        geo_adress="г. Ханты-Мансийск, Объездная 57а",
        flat_count=108,
        city_id=1,
    )

    house2 = House(
        id=15,
        name="Объездная 57",
        geo_adress="г. Ханты-Мансийск, Объездная 57",
        flat_count=122,
        city_id=1,
    )

    session.add_all([house1, house2])

    # ----- Входы для дома 13 -----
    entries_house1 = [
        Entry(id=101, name="Подъезд№1", flat_first=1, flat_last=54, house_id=13),
        Entry(id=102, name="Подъезд№2", flat_first=55, flat_last=108, house_id=13),
        Entry(id=103, name="Калитка", flat_first=1, flat_last=150, house_id=13),
    ]

    # ----- Входы для дома 15 -----
    entries_house2 = [
        Entry(id=201, name="Подъезд№1", flat_first=1, flat_last=50, house_id=15),
        Entry(id=202, name="Подъезд№2", flat_first=51, flat_last=122, house_id=15),
        Entry(id=203, name="Калитка", flat_first=1, flat_last=122, house_id=15),
    ]

    session.add_all(entries_house1 + entries_house2)

    intercoms = []

    fixed_tech_names = [
    "LWI-I0F-B3M-6RX",
    "9WN-I60-NCK-MM8",
    "XNM-YDF-R5Q-QW3",
    "P4J-VLK-TOI-C26",
    "51G-NL6-ELO-HGV",
    "ACT-FOD-IVO-P9R"
    ]

    
    for i,entry in entries_house1 + entries_house2:
        if i >= len(fixed_tech_names):
            break 
        intercoms.append(
            Intercom(
                name="Абрамс-1",
                tech_name=fixed_tech_names[i],
                entry_id=entry.id,
            )
        )

    session.add_all(intercoms)

    await session.commit()

    return {"status": "ok"}
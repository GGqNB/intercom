from typing import Type, Dict, Any, List

from faker import Faker
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

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
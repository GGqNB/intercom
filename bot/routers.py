import json

from request import get_user_settings, register_user, flat_by_number
from maxapi import Router, F
from maxapi.types import BotStarted, MessageCreated, MessageCallback, Command
import aiohttp
import re

from keyboards import (
    main_menu_kb,
    settings_menu_kb,
    houses_kb,
    confirm_flat_kb,
    HOUSE_MAP,
    confirm_menu_kb
)

router = Router()

user_states = {}

    
@router.message_created(Command("start"))
async def cmd_start(event: MessageCreated):
    await event.bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text="👋 Добро пожаловать!\n\nНажмите ⚙ Настройки.",
        attachments=[main_menu_kb()]
    )
@router.message_created()
async def handle_contact(event: MessageCreated):
    message = event.message
    body = message.body
    print(message.sender.user_id) 
    print(message.recipient.chat_id) 
    
    if not body or not body.attachments:
        return

    contact_att = next((att for att in body.attachments if att.type == "contact"), None)
    if not contact_att:
        return
    vcf_info = contact_att.payload.vcf_info
    max_info = contact_att.payload.max_info
    contact_user_id = max_info.user_id
    sender_user_id = message.sender.user_id

    if contact_user_id != sender_user_id:
        await event.bot.send_message(
            chat_id=message.recipient.chat_id,
            text="❌ Вы можете отправлять только свой контакт!"
        )
        return

    match = re.search(r"TEL;TYPE=\w+:(\+?\d+)", vcf_info)
    if match:
        phone_number = match.group(1)
        if phone_number.startswith('7'):
            phone_number = phone_number[1:]
    first_name = max_info.first_name
    last_name = max_info.last_name
    user_data = {
        "name": first_name,
        "chat_id": message.recipient.chat_id,
        "max_id": message.sender.user_id
    }
    await flat_by_number(phone_number, user_data)
    await event.bot.send_message(
        chat_id=message.recipient.chat_id,
        text=(
            f"✅ Контакт принят:\n"
            f"ID: {contact_user_id}\n"
            f"Имя: {first_name} {last_name}"
            f"Номер - {phone_number}"
        ),
    )

@router.bot_started()
async def handle_bot_started(event: BotStarted):
    user = event.user
    name = getattr(user, 'first_name', None) or 'друг'

    await event.bot.send_message(
        chat_id=event.chat_id,
        text= f"Добро пожаловать, {name} !\n\nНажмите ⚙ Настройки.",
        attachments=[main_menu_kb()]
    )

@router.message_callback(F.callback.payload == "cmd_home")
async def callback_home(event: MessageCallback):
    """Обработка кнопки Home"""
    chat_id = event.message.recipient.chat_id

    await event.answer(notification="🏠 Домашнее меню")

    await event.message.edit(
        text=(
            "🏠 Добро пожаловать на главную!\n\n"
            "Здесь вы можете вернуться к основным функциям бота.\n\n"
            "Чтобы увидеть текущие настройки, зайдите в '⚙ Настройки'"
        ),
        attachments=[main_menu_kb()]  # кнопка Home
    )

# --------------------
# ОТКРЫТЬ НАСТРОЙКИ
# --------------------

@router.message_callback(F.callback.payload == "cmd_settings")
async def callback_settings(event: MessageCallback):
    await event.answer(notification="⚙ Загружаем ваши настройки...")

    user_id = event.callback.user.user_id

    # 🔹 вызываем функцию из requests.py
    user_data = await get_user_settings(str(user_id))

    if not user_data:
        await event.message.edit(
            text="❌ Настройки не найдены",
            attachments=[settings_menu_kb()]
        )
        return

    flat_number = user_data.get("flat")
    house_id = user_data.get("house_id")
    name = user_data.get("name")

    house_text = next(
        (v["text"] for v in HOUSE_MAP.values() if v["id"] == house_id),
        "Неизвестный дом"
    )

    await event.message.edit(
        text=(
            f"⚙ Настройки пользователя\n\n"
            f"👤 Имя: {name}\n"
            f"🏠 Дом: {house_text}\n"
            f"🏢 Квартира: {flat_number}\n\n"
            "Выберите действие ниже:"
        ),
        attachments=[settings_menu_kb()]
    )


@router.message_callback(F.callback.payload == "cmd_choose_house")
async def callback_choose_house(event: MessageCallback):
    await event.answer()

    await event.message.edit(
        text="🏠 Выберите дом:",
        attachments=[houses_kb()]
    )


@router.message_callback(F.callback.payload.startswith("house_"))
async def callback_house_selected(event: MessageCallback):

    user_id = event.callback.user.user_id
    key = event.callback.payload 

    house_data = HOUSE_MAP.get(key)
    if not house_data:
        return

    user_states[user_id] = {
        "house_id": house_data["id"],
        "house_text": house_data["text"], 
        "step": "waiting_flat"
    }

    await event.answer()

    await event.message.edit(
        text=f"🏠 Дом {house_data['text']} выбран.\n\nВведите номер квартиры:",
        attachments=[]
    )


@router.message_created()
async def handle_flat_input(event: MessageCreated):

    user_id = event.message.sender.user_id

    if user_id not in user_states:
        return

    if user_states[user_id].get("step") != "waiting_flat":
        return

    flat_number = event.message.body.text

    if not flat_number or not flat_number.isdigit():
        await event.bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="❌ Введите номер квартиры (только цифры)."
        )
        return

    user_states[user_id]["flat_number"] = flat_number
    user_states[user_id]["step"] = "confirming"

    house_text = user_states[user_id]["house_text"]

    await event.bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text=(
            "Подтвердите выбор:\n\n"
            f"🏠 Дом: {house_text}\n" 
            f"🏢 Квартира: {flat_number}"
        ),
        attachments=[confirm_flat_kb()]
    )


@router.message_callback(F.callback.payload == "confirm_flat")
async def confirm_flat(event: MessageCallback):

    user_id = event.callback.user.user_id
    chat_id = event.message.recipient.chat_id
    name = event.callback.user.first_name

    data = user_states.get(user_id)
    if not data:
        return

    house_id = data["house_id"]
    house_text = data["house_text"]
    flat_number = int(data["flat_number"])

    payload = {
        "name": name,
        "chat_id": str(chat_id),
        "max_id": str(user_id),
        "flat": flat_number,
        "flat_stown": 0,
        "house_id": house_id
    }

    result = await register_user(payload)

    if not result["success"]:
        if result.get("error") == "Квартира не найдена":
            user_states[user_id]["step"] = "waiting_flat"

            await event.answer(notification="❌ Квартира не найдена")

            await event.message.edit(
                text=(
                    f"⚠ Возможно, вы ошиблись в номере квартиры.\n\n"
                    f"🏠 Дом: {house_text}\n\n"
                    f"Введите номер квартиры ещё раз:"
                ),
                attachments=[]
            )
            return

        await event.answer(notification="❌ Ошибка сервера")
        return

    user_states.pop(user_id, None)

    await event.answer(notification="✅ Сохранено")

    await event.message.edit(
        text=(
            f"✅ Настройки сохранены\n\n"
            f"🏠 Дом: {house_text}\n"
            f"🏢 Квартира: {flat_number}"
        ),
        attachments=[confirm_menu_kb()]
    )

@router.message_callback(F.callback.payload == "change_flat")
async def change_flat(event: MessageCallback):

    user_id = event.callback.user.user_id

    if user_id in user_states:
        user_states[user_id]["step"] = "waiting_flat"

    await event.answer()

    await event.message.edit(
        text="Введите номер квартиры заново:",
        attachments=[]
    )
    
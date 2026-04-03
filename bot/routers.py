import json

from request import call_open_door_backend, get_user_settings, register_user, flat_by_number
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
    confirm_menu_kb,
    reset_menu_kb
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

def get_house_text(house_id: int) -> str:
    for house in HOUSE_MAP.values():
        if house["id"] == house_id:
            return house["text"]
    return "Неизвестный дом"

@router.message_created()
async def handle_contact(event: MessageCreated):
    message = event.message
    body = message.body
    
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
            text="❌ Вы можете отправлять только свой контакт!\n\nЕсли хотите обновить свои данные о домах, нажмите Обновить данные",
            attachments=[reset_menu_kb()]
        )
        return

    match = re.search(r"TEL;TYPE=\w+:(\+?\d+)", vcf_info)
    if match:
        phone_number = match.group(1)
        if phone_number.startswith('7'):
            phone_number = phone_number[1:]
    print(phone_number)
    if phone_number != '9505024090' and phone_number != '9505010598':
        await event.bot.send_message(
        chat_id=message.recipient.chat_id,
        text=(
            f"Вам пока это не доступно\n"
        ), )
        return
    first_name = max_info.first_name
    last_name = max_info.last_name
    user_data = {
        "name": first_name,
        "chat_id": str(message.recipient.chat_id),
        "max_id": str(message.sender.user_id)
    }
    
    flats = await flat_by_number(phone_number, user_data)

    if flats and flats.get("data"):
        addresses = []

        for i, flat in enumerate(flats["data"], start=1):
            house_text = get_house_text(flat.get("house_id"))
            stown = flat.get("stown_flat", {})

            text = (
            f"{i}. {house_text}, "
            f"{stown.get('type', '')} {stown.get('number', '')}"
            )

            addresses.append(text)

        message_text = (
            "✅ Контакт принят:\n"
            "Ваши адреса:\n" +
            "\n".join(addresses)
        )

        await event.bot.send_message(
            chat_id=message.recipient.chat_id,
            text=message_text,
            attachments=[main_menu_kb()]
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


@router.message_callback(F.callback.payload == "cmd_settings")
async def callback_settings(event: MessageCallback):
    await event.answer(notification="⚙ Загружаем ваши настройки...")

    user_id = event.callback.user.user_id

    # 🔹 вызываем функцию
    user_list = await get_user_settings(str(user_id))

    # ❌ если список пустой или None
    if not user_list:
        await event.message.edit(
            text="❌ Настройки не найдены\n\n"+
            "Нажмите кнопку 'Обновить данные'",
            attachments=[settings_menu_kb()]
        )
        return

    # 🔹 быстрый мап для домов
    HOUSE_MAP_BY_ID = {v["id"]: v["text"] for v in HOUSE_MAP.values()}

    lines = []
    for i, user in enumerate(user_list, start=1):
        flat_number = user.get("flat")
        house_id = user.get("house_id")
        name = user.get("name")

        house_text = HOUSE_MAP_BY_ID.get(house_id, "Неизвестный дом")

        lines.append(
            f"{i}. 👤 {name}\n"
            f"   🏠 {house_text}\n"
            f"   🏢 Квартира: {flat_number}"
        )

    # 🔹 финальный текст
    message_text = (
        "⚙ Ваши настройки:\n\n" +
        "\n\n".join(lines) +
        "\n\nВыберите действие ниже:"
    )

    await event.message.edit(
        text=message_text,
        attachments=[settings_menu_kb()]
    )
    
@router.message_callback(F.callback.payload.startswith("open_door:"))
async def callback_open_door(event: MessageCallback):
    """
    Обработка кнопки 'Открыть' с удалением сообщения и ответом пользователю.
    """
    open_token = event.callback.payload.split(":", 1)[1]

    try:
        result = await call_open_door_backend(open_token)
        chat_id = event.message.recipient.chat_id

        if result.get("success"):
            text = "✅ Дверь успешно открыта!"
        else:
            text = result.get("error", "❌ Не удалось открыть дверь")

        await event.message.edit(
            text=text,
            attachments=[confirm_menu_kb()]
        )

    except Exception as e:
        await event.message.edit(
            text=f"❌ Произошла ошибка: Обратитесь к администратору",
            attachments=[confirm_menu_kb()]
        )
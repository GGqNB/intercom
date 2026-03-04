from request import register_user
from maxapi import Router, F
from maxapi.types import MessageCreated, MessageCallback, Command
import aiohttp

from keyboards import (
    main_menu_kb,
    settings_menu_kb,
    houses_kb,
    confirm_flat_kb,
    HOUSE_MAP
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


# --------------------
# ОТКРЫТЬ НАСТРОЙКИ
# --------------------

@router.message_callback(F.callback.payload == "cmd_settings")
async def callback_settings(event: MessageCallback):
    await event.answer()

    await event.message.edit(
        text="⚙ Настройки\n\nВыберите дом:",
        attachments=[settings_menu_kb()]
    )


# --------------------
# ПОКАЗАТЬ ДОМА
# --------------------

@router.message_callback(F.callback.payload == "cmd_choose_house")
async def callback_choose_house(event: MessageCallback):
    await event.answer()

    await event.message.edit(
        text="🏠 Выберите дом:",
        attachments=[houses_kb()]
    )


# --------------------
# ДОМ ВЫБРАН
# --------------------

@router.message_callback(F.callback.payload.startswith("house_"))
async def callback_house_selected(event: MessageCallback):

    user_id = event.callback.user.user_id
    key = event.callback.payload  # например 'house_1'

    house_data = HOUSE_MAP.get(key)
    if not house_data:
        return

    user_states[user_id] = {
        "house_id": house_data["id"],   # для сервера
        "house_text": house_data["text"],  # для отображения пользователю
        "step": "waiting_flat"
    }

    await event.answer()

    await event.message.edit(
        text=f"🏠 Дом {house_data['text']} выбран.\n\nВведите номер квартиры:",
        attachments=[]
    )


# --------------------
# ВВОД КВАРТИРЫ
# --------------------


@router.message_created()
async def handle_flat_input(event: MessageCreated):

    user_id = event.message.sender.user_id

    if user_id not in user_states:
        return

    if user_states[user_id].get("step") != "waiting_flat":
        return

    # берем текст квартиры
    flat_number = event.message.body.text

    if not flat_number or not flat_number.isdigit():
        await event.bot.send_message(
            chat_id=event.message.recipient.chat_id,
            text="❌ Введите номер квартиры (только цифры)."
        )
        return

    # сохраняем квартиру и меняем шаг
    user_states[user_id]["flat_number"] = flat_number
    user_states[user_id]["step"] = "confirming"

    # берем текст дома для пользователя
    house_text = user_states[user_id]["house_text"]

    await event.bot.send_message(
        chat_id=event.message.recipient.chat_id,
        text=(
            "Подтвердите выбор:\n\n"
            f"🏠 Дом: {house_text}\n"  # показываем адрес, а не id
            f"🏢 Квартира: {flat_number}"
        ),
        attachments=[confirm_flat_kb()]
    )

# --------------------
# ПОДТВЕРЖДЕНИЕ
# --------------------

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

    del user_states[user_id]

    # 🔹 Формируем объект для бэка
    payload = {
        "name": name,
        "chat_id": str(chat_id),
        "max_id": str(user_id),
        "flat": flat_number,
        "house_id": house_id
    }

    success = await register_user(payload)

    if not success:
        await event.answer(notification="❌ Ошибка сохранения")
        return

    del user_states[user_id]


    await event.answer(notification="✅ Сохранено")

    await event.message.edit(
        text=(
            f"✅ Настройки сохранены\n\n"
            f"🏠 Дом: {house_text}\n"
            f"🏢 Квартира: {flat_number}"
        ),
        attachments=[main_menu_kb()]
    )


# --------------------
# ИЗМЕНИТЬ
# --------------------

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
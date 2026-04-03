from maxapi.types import CallbackButton, ButtonsPayload, Attachment, RequestContactButton
from maxapi.enums.intent import Intent


def main_menu_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                    CallbackButton(
                        text="⚙ Настройки",
                        payload="cmd_settings",
                        intent=Intent.DEFAULT
                    )
                ]
            ]
        )
    )

def open_door_kb(open_token: str) -> Attachment:
    """
    Клавиатура с одной кнопкой 'Открыть', payload = токен.
    """
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                    CallbackButton(
                        text="Открыть",
                        payload='open_door:'+open_token,  # обязательно непустой payload
                        intent=Intent.DEFAULT
                    )
                ]
            ]
        )
    )
def confirm_menu_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                    CallbackButton(
                        text="⚙ Настройки",
                        payload="cmd_settings",
                        intent=Intent.DEFAULT
                    ),
                    CallbackButton(
                        text="🏠 Главная",
                        payload="cmd_home",
                        intent=Intent.DEFAULT
                    ),
                ]
            ]
        )
    )

def reset_menu_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                      RequestContactButton(
                        text="Обновить данные",
                        payload="request_contact",
                        intent=Intent.DEFAULT
                    )
                ]
            ]
        )
    )

def settings_menu_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                      RequestContactButton(
                        text="Обновить данные",
                        payload="request_contact",
                        intent=Intent.DEFAULT
                    )
                ],
                [
                     CallbackButton(
                        text="🏠 Главная",
                        payload="cmd_home",
                        intent=Intent.DEFAULT
                    ),
                ]
            ]
        )
    )

HOUSE_MAP = {
    "house_1": {"id": 15, "text": "Объездная 57"},
    "house_2": {"id": 13, "text": "Объездная 57А"}
}

def houses_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                    CallbackButton(
                        text=HOUSE_MAP["house_1"]["text"],
                        payload="house_1",
                        intent=Intent.DEFAULT
                    ),
                    CallbackButton(
                        text=HOUSE_MAP["house_2"]["text"],
                        payload="house_2",
                        intent=Intent.DEFAULT
                    )
                ]
            ]
        )
    )


def confirm_flat_kb():
    return Attachment(
        type="inline_keyboard",
        payload=ButtonsPayload(
            buttons=[
                [
                    CallbackButton(
                        text="✅ Подтвердить",
                        payload="confirm_flat",
                        intent=Intent.POSITIVE
                    ),
                    CallbackButton(
                        text="❌ Изменить",
                        payload="change_flat",
                        intent=Intent.NEGATIVE
                    )
                ]
            ]
        )
    )
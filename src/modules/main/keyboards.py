from core.helpers import build_menu

CAN_I_SMOKE_BUTTON_TEXT = '🚬Хочу пыхнуть'
I_SMOKED_BUTTON_TEXT = '☠️Я пыхнул'
SETTINGS_BUTTON_TEXT = '⚙️Настройки'


def get_start_keyboard():
    buttons = [
        CAN_I_SMOKE_BUTTON_TEXT,
        I_SMOKED_BUTTON_TEXT
    ]
    footer_button = SETTINGS_BUTTON_TEXT
    return build_menu(buttons, footer_button=footer_button)

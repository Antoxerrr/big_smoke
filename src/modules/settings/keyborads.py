from core.db.models import User
from core.helpers import build_menu
from core.keyboards import BACK_BUTTON_TEXT

# Кнопки основного меню
from smoking.helpers import get_user_mode_id
from smoking.mode import EasyMode, NormalMode, HardMode

START_PROGRAM_BUTTON_TEXT = '🟢 Начать работу'
STOP_PROGRAM_BUTTON_TEXT = '🔴 Остановить работу'
SWITCH_MODE_BUTTON_TEXT = '🔵 Изменить режим'

# Кнопки меню "Начать работу"
EASY_MODE_BUTTON_TEXT = '🐣 Лёгкий'
NORMAL_MODE_BUTTON_TEXT = '🐥 Обычный'
HARD_MODE_BUTTON_TEXT = '🐓 Тяжёлый'

# Кнопки меню "Остановить работу"
APPLY_STOP_BUTTON_TEXT = '✅'
CANCEL_STOP_BUTTON_TEXT = '❌'


MODE_KEYBOARD_BUTTONS_MAP = {
    EasyMode.mode_id: EASY_MODE_BUTTON_TEXT,
    NormalMode.mode_id: NORMAL_MODE_BUTTON_TEXT,
    HardMode.mode_id: HARD_MODE_BUTTON_TEXT
}


def get_settings_keyboard(user: User):
    """Клавиатура настроек.

    Отображает клавиатуру в зависимости от того,
    запущена ли программа бота у пользователя.
    """
    if not user.program_is_active:
        buttons = [START_PROGRAM_BUTTON_TEXT]
    else:
        buttons = [STOP_PROGRAM_BUTTON_TEXT, SWITCH_MODE_BUTTON_TEXT]
    return build_menu(buttons, footer_button=BACK_BUTTON_TEXT)


def get_mode_list_keyboard(user: User):
    """Клавиатура с кнопками выбора режима."""
    mode_id = get_user_mode_id(user)
    buttons = [
        EASY_MODE_BUTTON_TEXT, NORMAL_MODE_BUTTON_TEXT, HARD_MODE_BUTTON_TEXT
    ]
    if mode_id and user.program_is_active:
        button_to_remove = MODE_KEYBOARD_BUTTONS_MAP.get(mode_id)
        if button_to_remove:
            buttons.remove(button_to_remove)
    return build_menu(buttons, footer_button=BACK_BUTTON_TEXT)


def get_stop_program_user_ask_keyboard():
    """Клавиатура для подтверждения операции остановки работы программы."""
    buttons = [CANCEL_STOP_BUTTON_TEXT, APPLY_STOP_BUTTON_TEXT]
    return build_menu(buttons)

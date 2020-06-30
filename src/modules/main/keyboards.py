from core.db.models import User
from core.helpers import build_menu, user_program_is_active

CAN_I_SMOKE_BUTTON_TEXT = 'Когда можно❓'
I_SMOKED_BUTTON_TEXT = '☠ Update! ️☠️'
SETTINGS_BUTTON_TEXT = '⚙️Настройки'


def get_start_keyboard(user: User):
    buttons = []
    if user_program_is_active(user):
        buttons = [
            CAN_I_SMOKE_BUTTON_TEXT,
            I_SMOKED_BUTTON_TEXT
        ]
    footer_button = SETTINGS_BUTTON_TEXT
    return build_menu(buttons, footer_button=footer_button)

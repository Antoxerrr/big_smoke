from core.db.models import User
from core.helpers import build_menu

START_PROGRAM_BUTTON = 'Начать работу'
STOP_PROGRAM_BUTTON = 'Остановить работу'


def get_settings_keyboard(user: User):
    """Клавиатура настроек."""
    # Главная кнопка - начать или остановить работу,
    # в зависимости от пользователя
    main_button = (
        START_PROGRAM_BUTTON
        if not user.date_start
        else STOP_PROGRAM_BUTTON
    )
    return build_menu([main_button])

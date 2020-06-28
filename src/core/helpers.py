from datetime import datetime

from mongoengine import DoesNotExist
from telegram import ReplyKeyboardMarkup

from core.db.models import User
from core.exceptions import UserNotFoundUnexpectedError
from smoking.mode import EasyMode, NormalMode, HardMode


def build_menu(
        buttons: list,
        columns: int = 3,
        header_button=None,
        footer_button=None,
        resize_keyboard: bool = True
):
    """Хелпер для удобного построения меню."""
    menu = [buttons[i:i + columns] for i in range(0, len(buttons), columns)]
    if header_button:
        menu.insert(0, [header_button])
    if footer_button:
        menu.append([footer_button])

    return ReplyKeyboardMarkup(menu, resize_keyboard=resize_keyboard)


def get_user_or_raise(user_id):
    """Получает юзера или рейзит кастомную ошибку."""
    try:
        user = User.objects.get(user_id=user_id)
    except DoesNotExist:
        raise UserNotFoundUnexpectedError()
    return user


def enable_mode(user: User, mode_id: int, starting: bool = True):
    """Функция активации режима работы программы.

    Флаг starting отвечает за то, начинает ли пользователь
    работу с программой бота или же просто меняет режим.
    """
    user.mode_id = mode_id
    if starting:
        user.date_start = user.last_smoked = datetime.now()
    user.save()


def get_mode_id_by_button_text(button_text):
    from modules.settings.keyborads import (
        HARD_MODE_BUTTON_TEXT, NORMAL_MODE_BUTTON_TEXT, EASY_MODE_BUTTON_TEXT
    )
    mode_id = None
    if button_text == EASY_MODE_BUTTON_TEXT:
        mode_id = EasyMode.mode_id
    elif button_text == NORMAL_MODE_BUTTON_TEXT:
        mode_id = NormalMode.mode_id
    elif button_text == HARD_MODE_BUTTON_TEXT:
        mode_id = HardMode.mode_id
    return mode_id

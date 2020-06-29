from datetime import datetime
from typing import List

import sentry_sdk
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
        exception = UserNotFoundUnexpectedError()
        sentry_sdk.capture_exception(exception)
        raise exception
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


def user_program_is_active(user: User) -> bool:
    """Проверка, активна ли у юзера программа бота в данный момент."""
    return (user.date_start is not None) and (user.mode_id is not None)


def decide_declension(variants: List[str], number: int):
    """Подбирает нужное склонение для слова."""
    if not len(variants) == 3:
        raise ValueError('Длина списка вариантов должна быть равна трём.')

    if number % 10 == 1 and not (10 < number < 20):
        result = variants[0]
    elif 2 <= number <= 4 or (number > 20 and 2 <= (number % 10) <= 4):
        result = variants[1]
    else:
        result = variants[2]
    return result

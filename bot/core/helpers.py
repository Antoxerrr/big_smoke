from typing import List

from telegram import ReplyKeyboardMarkup
from tortoise import timezone
from tortoise.exceptions import DoesNotExist

from bot.core.exceptions import UserNotFoundUnexpectedError
from bot.db.models import User, ModeUsage
from bot.smoking.mode import EasyMode, NormalMode, HardMode


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


async def get_user_or_raise(user_id: int) -> User:
    """Получает юзера или рейзит кастомную ошибку."""
    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        exception = UserNotFoundUnexpectedError()
        raise exception
    return user


async def enable_mode(user: User, mode_id: int):
    """Функция активации режима работы программы."""
    now = timezone.now()
    actual_mode_usage = await ModeUsage.filter(
        user=user, date_end=None
    ).first()

    # Закрываем работу прошлого режима
    if actual_mode_usage:
        actual_mode_usage.date_end = now
        await actual_mode_usage.save()

    # Начинаем работу нового режима
    await ModeUsage.create(user=user, mode_id=mode_id, date_start=now)

    if not user.program_is_active:
        user.program_is_active = True
        user.last_smoked = now
        await user.save()


def get_mode_id_by_button_text(button_text):
    from bot.modules.settings.keyboards import (
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

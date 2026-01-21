from datetime import datetime

from tortoise import timezone

from telegram import User as TelegramUser

from bot.core.helpers import decide_declension
from bot.db.models import User
from bot.modules.main.const import HOUR_VARIANTS, MINUTE_VARIANTS


async def get_or_create_user(telegram_user: TelegramUser) -> User:
    user, _created = await User.get_or_create(id=telegram_user.id)
    return user


def get_verbose_string_time_remaining(seconds):
    hours_str = minutes_str = None

    hours = seconds // 3600
    if not hours == 0:
        hours_str = f'**{hours} {decide_declension(HOUR_VARIANTS, hours)}**'
    seconds %= 3600

    minutes = seconds // 60
    if not minutes == 0:
        minutes_str = (
            f'**{minutes} {decide_declension(MINUTE_VARIANTS, minutes)}**'
        )
    seconds %= 60

    if hours == 0 and minutes == 0:
        answer = 'До следующего раза меньше минуты.'
    else:
        answer_list = []
        if hours_str:
            answer_list.append(hours_str)
        if minutes_str:
            answer_list.append(minutes_str)
        answer = ' и '.join(answer_list)
        answer = 'До следующего раза ' + answer
    return answer


def beautiful_smoke_ask_answer(next_smoke_time: datetime) -> str:
    """Форматирует строку даты в зависимости от того насколько она 'далеко'."""
    now = timezone.now()
    if now > next_smoke_time:
        result = None
    else:
        delta = next_smoke_time - now
        # Если день и больше
        if delta.days > 0:
            result = next_smoke_time.strftime('%d.%m.%Y %H:%M')
            result = 'Следующий раз: *%s*' % result
        else:
            result = get_verbose_string_time_remaining(delta.seconds)
    return result + ' ❌'

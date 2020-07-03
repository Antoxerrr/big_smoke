from datetime import datetime

import sentry_sdk
from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler

from core.db.models import User
from core.exceptions import DateSmokedGreaterThanToday
from core.filters import CustomFilters
from core.helpers import get_user_or_raise
from core.telegram import dispatcher
from modules.main import messages
from modules.main.helpers import get_or_create_user, beautiful_smoke_ask_answer
from modules.main.keyboards import (
    get_start_keyboard, CAN_I_SMOKE_BUTTON_TEXT, I_SMOKED_BUTTON_TEXT
)
from smoking.calculator import SmokingTimeCalculator


def start(update, context):
    """Обработчик команды start."""
    user = get_or_create_user(update.effective_user)
    keyboard = get_start_keyboard(user)
    update.message.reply_markdown(
        messages.HELLO_START_MESSAGE, reply_markup=keyboard
    )


def check_user_last_smoke_date(user: User):
    if user.last_smoked > datetime.now():
        exception = DateSmokedGreaterThanToday()
        sentry_sdk.capture_exception(exception)
        raise exception


def smoke_asking(update, context):
    """Обработка кнопки 'Можно курить?'."""
    user = get_user_or_raise(update.effective_user.id)
    if user.program_is_active:
        check_user_last_smoke_date(user)
        next_smoke_time, smoking_allowed = SmokingTimeCalculator.calculate(
            user
        )
        if smoking_allowed:
            update.message.reply_text(messages.YOU_CAN_SMOKE_MESSAGE)
        else:
            answer = beautiful_smoke_ask_answer(next_smoke_time)
            update.message.reply_text(
                answer, parse_mode=ParseMode.MARKDOWN
            )


def smoke_update(update, context):
    """Обработка кнопки 'Я покурил'."""
    user = get_user_or_raise(update.effective_user.id)
    if user.program_is_active:
        user.last_smoked = datetime.now()
        user.save()
        update.message.reply_text(messages.TIMER_IS_UPDATED_MESSAGE)


def _write_shit(error_msg):
    with open('/logs/errors.txt', 'a') as file:
        file.write('\n' + error_msg)


def on_error(update, context):
    """Обработчик ошибок."""
    error_msg = str(context.error)
    _write_shit(error_msg)
    message = (
        f'{messages.AN_ERROR_OCCURRED_MESSAGE} \n\n `{error_msg}`'
    )
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


def help_cmd(update, context):
    """Обработчик команды /help."""
    update.message.reply_text(
        messages.HELP_TEXT, parse_mode=ParseMode.MARKDOWN
    )


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_cmd))
dispatcher.add_handler(
    MessageHandler(
        CustomFilters.button(CAN_I_SMOKE_BUTTON_TEXT),
        smoke_asking
    )
)
dispatcher.add_handler(
    MessageHandler(
        CustomFilters.button(I_SMOKED_BUTTON_TEXT),
        smoke_update
    )
)
dispatcher.add_error_handler(on_error)

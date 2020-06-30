from datetime import datetime

import sentry_sdk
from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler

from core.db.models import User
from core.exceptions import DateSmokedGreaterThanToday
from core.filters import CustomFilters
from core.helpers import get_user_or_raise, user_program_is_active
from core.telegram import dispatcher
from modules.main import messages
from modules.main.helpers import get_or_create_user, beautiful_smoke_ask_answer
from modules.main.keyboards import (
    get_start_keyboard, CAN_I_SMOKE_BUTTON_TEXT, I_SMOKED_BUTTON_TEXT
)
from smoking.modes_map import modes_map


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
    if user_program_is_active(user):
        check_user_last_smoke_date(user)
        mode = modes_map.get(user.mode_id)
        if mode:
            next_smoke_time, smoking_allowed = mode.ask_for_smoke(
                user.date_start, user.last_smoked
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
    if user_program_is_active(user):
        user.last_smoked = datetime.now()
        user.save()
        update.message.reply_text(messages.TIMER_IS_UPDATED_MESSAGE)


def on_error(update, context):
    """Обработчик ошибок."""
    error_msg = str(context.error)
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

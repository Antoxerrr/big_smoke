from telegram.ext import CommandHandler, MessageHandler

from core.exceptions import UserNotFoundUnexpectedError
from core.filters import CustomFilters
from core.telegram import dispatcher
from modules.main.helpers import get_or_create_user
from modules.main.keyboards import (
    get_start_keyboard, CAN_I_SMOKE_BUTTON_TEXT, I_SMOKED_BUTTON_TEXT
)


def start(update, context):
    """Обработчик команды start."""
    get_or_create_user(update.effective_user)
    keyboard = get_start_keyboard()
    update.message.reply_markdown('Привет!', reply_markup=keyboard)


def smoke_asking(update, context):
    """Обработка кнопки 'Можно курить?'."""
    update.message.reply_text('Нет бля')


def smoke_update(update, context):
    """Обработка кнопки 'Я покурил'."""
    update.message.reply_text('Ну ты и дебил...')


def on_error(update, context):
    """Обработчик ошибок."""
    update.message.reply_text('Произошла ошибка ;(')


dispatcher.add_handler(CommandHandler('start', start))
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

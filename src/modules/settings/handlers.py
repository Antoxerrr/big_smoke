from mongoengine import DoesNotExist
from telegram.ext import ConversationHandler, MessageHandler

from core.db.models import User
from core.filters import CustomFilters
from core.keyboards import BACK_BUTTON_TEXT, BACK_FILTER
from core.telegram import dispatcher
from modules.main.keyboards import SETTINGS_BUTTON_TEXT, get_start_keyboard
from modules.settings.keyborads import get_settings_keyboard


SETTINGS_STATE = range(1)


def settings(update, context):
    """Корневой обработчик меню настроек."""
    try:
        user = User.objects.get(user_id=update.effective_user.id)
    except DoesNotExist:
        return
    keyboard = get_settings_keyboard(user)
    update.message.reply_text(
        'Добро пожаловать в настройки!', reply_markup=keyboard
    )
    return SETTINGS_STATE


def start_program(update, context):
    """Обработчик начала работы программы."""


def stop_program(update, context):
    """Обработчик остановки работы программы."""


def switch_mode(update, context):
    """Обработчик переключения режима работы программы."""


def back(update, context):
    """Кнопка назад."""
    update.message.reply_text('Ахуеть.', reply_markup=get_start_keyboard())
    return ConversationHandler.END


dispatcher.add_handler(
    ConversationHandler(
        entry_points=[
            MessageHandler(
                filters=CustomFilters.button(SETTINGS_BUTTON_TEXT),
                callback=settings,
            )
        ],
        states={

        },
        fallbacks=[
            MessageHandler(BACK_FILTER, back)
        ],
        allow_reentry=True
    )
)

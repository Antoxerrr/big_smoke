from functools import partial

from telegram import ParseMode
from telegram.ext import ConversationHandler, MessageHandler

from core.db.models import ModeUsage
from core.filters import CustomFilters
from core.helpers import (
    get_user_or_raise, enable_mode, get_mode_id_by_button_text
)
from core.keyboards import BACK_FILTER
from core.telegram import dispatcher
from modules.main.keyboards import SETTINGS_BUTTON_TEXT, get_start_keyboard
from modules.settings import messages
from modules.settings.keyborads import (
    get_settings_keyboard, START_PROGRAM_BUTTON_TEXT, SWITCH_MODE_BUTTON_TEXT,
    STOP_PROGRAM_BUTTON_TEXT, get_mode_list_keyboard,
    get_stop_program_user_ask_keyboard, EASY_MODE_BUTTON_TEXT,
    NORMAL_MODE_BUTTON_TEXT, HARD_MODE_BUTTON_TEXT, APPLY_STOP_BUTTON_TEXT,
    CANCEL_STOP_BUTTON_TEXT
)

SETTINGS, STARTING, STOPPING, SWITCHING_MODE = range(4)
MODE_BUTTONS_FILTER = (
    CustomFilters.button(EASY_MODE_BUTTON_TEXT)
    | CustomFilters.button(NORMAL_MODE_BUTTON_TEXT)
    | CustomFilters.button(HARD_MODE_BUTTON_TEXT)
)


def settings(update, context, message: str = None):
    """Корневой обработчик меню настроек."""
    message = message if message else messages.SETTINGS_MESSAGE
    user = get_user_or_raise(update.effective_user.id)
    keyboard = get_settings_keyboard(user)
    update.message.reply_text(
        message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN
    )
    return SETTINGS


def start_program(update, context):
    """Обработчик начала работы программы или переключения режима."""
    user = get_user_or_raise(update.effective_user.id)
    update.message.reply_text(
        messages.CHOOSE_MODE_MESSAGE,
        reply_markup=get_mode_list_keyboard(user)
    )
    return STARTING


def back_to_settings(update, context, *args, **kwargs):
    """Возвращает в меню настроек."""
    message = kwargs.get('message')
    return settings(update, context, message=message)


def perform_start(update, context):
    """Обработка выбранного режима и начало работы юзера с программой бота."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = get_user_or_raise(update.effective_user.id)
    if mode_id:
        message = messages.build_mode_is_set_message(mode_id)
        enable_mode(user, mode_id)
        return settings(update, context, message=message)


def stop_program(update, context):
    """Обработчик остановки работы программы."""
    update.message.reply_text(
        messages.ARE_YOU_SURE_MESSAGE,
        reply_markup=get_stop_program_user_ask_keyboard()
    )
    return STOPPING


def stopping_apply(update, context):
    """Остановка работы программы для юзера."""
    user = get_user_or_raise(update.effective_user.id)
    user.last_smoked = None
    user.program_is_active = False
    user.save()

    # Удаляем все записи по режимам
    ModeUsage.objects(user=user).delete()
    return settings(update, context, message=messages.PROGRAM_STOPPED_MESSAGE)


def switch_mode(update, context):
    """Меню переключения режима работы."""
    user = get_user_or_raise(update.effective_user.id)
    update.message.reply_text(
        messages.CHOOSE_MODE_MESSAGE,
        reply_markup=get_mode_list_keyboard(user)
    )
    return SWITCHING_MODE


def perform_switch_mode(update, context):
    """Обработчик переключения режима работы программы."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = get_user_or_raise(update.effective_user.id)
    if mode_id:
        message = messages.build_mode_is_set_message(mode_id)
        enable_mode(user, mode_id)
        return settings(update, context, message=message)


def back(update, context):
    """Кнопка назад."""
    user = get_user_or_raise(update.effective_user.id)
    update.message.reply_text(
        messages.MAIN_MENU_MESSAGE, reply_markup=get_start_keyboard(user)
    )
    return ConversationHandler.END


stopping_decline = partial(
    back_to_settings, message=messages.PROGRAM_STOPPING_CANCELED_MESSAGE
)

dispatcher.add_handler(
    ConversationHandler(
        entry_points=[
            MessageHandler(
                filters=CustomFilters.button(SETTINGS_BUTTON_TEXT),
                callback=settings,
            )
        ],
        states={
            SETTINGS: [
                MessageHandler(
                    CustomFilters.button(START_PROGRAM_BUTTON_TEXT),
                    start_program
                ),
                MessageHandler(
                    CustomFilters.button(STOP_PROGRAM_BUTTON_TEXT),
                    stop_program
                ),
                MessageHandler(
                    CustomFilters.button(SWITCH_MODE_BUTTON_TEXT),
                    switch_mode
                ),
                MessageHandler(BACK_FILTER, back)
            ],
            STARTING: [
                MessageHandler(MODE_BUTTONS_FILTER, perform_start),
                MessageHandler(BACK_FILTER, back_to_settings)
            ],
            STOPPING: [
                MessageHandler(
                    CustomFilters.button(APPLY_STOP_BUTTON_TEXT),
                    stopping_apply
                ),
                MessageHandler(
                    CustomFilters.button(CANCEL_STOP_BUTTON_TEXT),
                    stopping_decline
                )
            ],
            SWITCHING_MODE: [
                MessageHandler(MODE_BUTTONS_FILTER, perform_switch_mode),
                MessageHandler(BACK_FILTER, back_to_settings)
            ]
        },
        fallbacks=[
            MessageHandler(BACK_FILTER, back)
        ],
        allow_reentry=True
    )
)

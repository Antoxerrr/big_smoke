from telegram.ext import ConversationHandler, MessageHandler

from core.filters import CustomFilters
from core.helpers import (
    get_user_or_raise, enable_mode, get_mode_id_by_button_text
)
from core.keyboards import BACK_FILTER
from core.telegram import dispatcher
from modules.main.keyboards import SETTINGS_BUTTON_TEXT, get_start_keyboard
from modules.settings.keyborads import (
    get_settings_keyboard, START_PROGRAM_BUTTON_TEXT, SWITCH_MODE_BUTTON_TEXT,
    STOP_PROGRAM_BUTTON_TEXT, get_mode_list_keyboard,
    get_stop_program_user_ask_keyboard, EASY_MODE_BUTTON_TEXT,
    NORMAL_MODE_BUTTON_TEXT, HARD_MODE_BUTTON_TEXT, APPLY_STOP_BUTTON_TEXT,
    CANCEL_STOP_BUTTON_TEXT
)

SETTINGS, STARTING, STOPPING, SWITCHING_MODE = range(4)
MODE_BUTTONS_FILTER = (
        CustomFilters.button(EASY_MODE_BUTTON_TEXT) |
        CustomFilters.button(NORMAL_MODE_BUTTON_TEXT) |
        CustomFilters.button(HARD_MODE_BUTTON_TEXT)
)


def settings(update, context):
    """Корневой обработчик меню настроек."""
    user = get_user_or_raise(update.effective_user.id)
    keyboard = get_settings_keyboard(user)
    update.message.reply_text(
        'Добро пожаловать в настройки!', reply_markup=keyboard
    )
    return SETTINGS


def start_program(update, context):
    """Обработчик начала работы программы или переключения режима."""
    update.message.reply_text(
        'Выберите режим работы программы.',
        reply_markup=get_mode_list_keyboard()
    )
    return STARTING


def back_to_settings(update, context):
    """Возвращает в меню настроек."""
    return settings(update, context)


def perform_start(update, context):
    """Обработка выбранного режима и начало работы юзера с программой бота."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = get_user_or_raise(update.effective_user.id)
    if mode_id:
        enable_mode(user, mode_id)
        return settings(update, context)


def stop_program(update, context):
    """Обработчик остановки работы программы."""
    update.message.reply_text(
        'Вы уверены?', reply_markup=get_stop_program_user_ask_keyboard()
    )
    return STOPPING


def stopping_apply(update, context):
    """Остановка работы программы для юзера."""
    user = get_user_or_raise(update.effective_user.id)
    user.date_start = None
    user.last_smoked = None
    user.mode_id = None
    user.save()
    return settings(update, context)


def switch_mode(update, context):
    """Меню переключения режима работы."""
    update.message.reply_text(
        'Выберите режим работы программы.',
        reply_markup=get_mode_list_keyboard()
    )
    return SWITCHING_MODE


def perform_switch_mode(update, context):
    """Обработчик переключения режима работы программы."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = get_user_or_raise(update.effective_user.id)
    if mode_id:
        enable_mode(user, mode_id, starting=False)
        return settings(update, context)


def back(update, context):
    """Кнопка назад."""
    user = get_user_or_raise(update.effective_user.id)
    update.message.reply_text(
        'Главное меню', reply_markup=get_start_keyboard(user)
    )
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
                    back_to_settings
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

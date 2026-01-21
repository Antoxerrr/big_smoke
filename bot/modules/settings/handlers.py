from telegram.constants import ParseMode
from telegram.ext import ConversationHandler, MessageHandler

from bot.core.filters import button
from bot.core.helpers import (
    get_user_or_raise, enable_mode, get_mode_id_by_button_text
)
from bot.core.keyboards import BACK_FILTER
from bot.db.models import ModeUsage
from bot.modules.main.keyboards import SETTINGS_BUTTON_TEXT, get_start_keyboard
from bot.modules.settings import messages
from bot.modules.settings.keyboards import (
    get_settings_keyboard, START_PROGRAM_BUTTON_TEXT, SWITCH_MODE_BUTTON_TEXT,
    STOP_PROGRAM_BUTTON_TEXT, get_mode_list_keyboard,
    get_stop_program_user_ask_keyboard, EASY_MODE_BUTTON_TEXT,
    NORMAL_MODE_BUTTON_TEXT, HARD_MODE_BUTTON_TEXT, APPLY_STOP_BUTTON_TEXT,
    CANCEL_STOP_BUTTON_TEXT, INTERVALS_BUTTON_TEXT
)
from bot.smoking.helpers import get_user_mode_id
from bot.smoking.modes_map import modes_map

SETTINGS, STARTING, STOPPING, SWITCHING_MODE = range(4)
MODE_BUTTONS_FILTER = (
    button(EASY_MODE_BUTTON_TEXT)
    | button(NORMAL_MODE_BUTTON_TEXT)
    | button(HARD_MODE_BUTTON_TEXT)
)


async def settings(update, context, message: str = None):
    """Корневой обработчик меню настроек."""
    message = message if message else messages.SETTINGS_MESSAGE
    user = await get_user_or_raise(update.effective_user.id)
    keyboard = await get_settings_keyboard(user)
    await update.message.reply_text(
        message, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN
    )
    return SETTINGS


def format_interval_minutes(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    parts = []
    if hours:
        parts.append(f'{hours} ч')
    if minutes or not parts:
        parts.append(f'{minutes} мин')
    return ' '.join(parts)


def build_intervals_message(mode_id: int) -> str:
    mode = modes_map.get(mode_id)
    if not mode:
        return 'Не удалось определить текущий режим.'
    lines = [f'Интервалы режима *{mode.name}* (дни 1-60):']
    for day in range(1, 61):
        minutes = round(mode.calculate_interval(day) * 60)
        lines.append(f'{day} день - {format_interval_minutes(minutes)}')
    return '\n'.join(lines)


async def show_intervals(update, context):
    user = await get_user_or_raise(update.effective_user.id)
    mode_id = await get_user_mode_id(user)
    if not mode_id:
        await update.message.reply_text(
            'Сначала выберите режим работы.',
            parse_mode=ParseMode.MARKDOWN,
        )
        return SETTINGS
    await update.message.reply_text(
        build_intervals_message(mode_id), parse_mode=ParseMode.MARKDOWN
    )
    return SETTINGS


async def start_program(update, context):
    """Обработчик начала работы программы или переключения режима."""
    user = await get_user_or_raise(update.effective_user.id)
    await update.message.reply_text(
        messages.CHOOSE_MODE_MESSAGE,
        reply_markup=await get_mode_list_keyboard(user)
    )
    return STARTING


async def back_to_settings(update, context, *args, **kwargs):
    """Возвращает в меню настроек."""
    message = kwargs.get('message')
    return await settings(update, context, message=message)


async def perform_start(update, context):
    """Обработка выбранного режима и начало работы юзера с программой бота."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = await get_user_or_raise(update.effective_user.id)
    if mode_id:
        message = messages.build_mode_is_set_message(mode_id)
        await enable_mode(user, mode_id)
        return await settings(update, context, message=message)


async def stop_program(update, context):
    """Обработчик остановки работы программы."""
    await update.message.reply_text(
        messages.ARE_YOU_SURE_MESSAGE,
        reply_markup=get_stop_program_user_ask_keyboard()
    )
    return STOPPING


async def stopping_apply(update, context):
    """Остановка работы программы для юзера."""
    user = await get_user_or_raise(update.effective_user.id)
    user.last_smoked = None
    user.program_is_active = False
    await user.save()

    # Удаляем все записи по режимам
    await ModeUsage.filter(user=user).delete()
    return await settings(update, context, message=messages.PROGRAM_STOPPED_MESSAGE)


async def switch_mode(update, context):
    """Меню переключения режима работы."""
    user = await get_user_or_raise(update.effective_user.id)
    await update.message.reply_text(
        messages.CHOOSE_MODE_MESSAGE,
        reply_markup=await get_mode_list_keyboard(user)
    )
    return SWITCHING_MODE


async def perform_switch_mode(update, context):
    """Обработчик переключения режима работы программы."""
    mode_id = get_mode_id_by_button_text(update.message.text)
    user = await get_user_or_raise(update.effective_user.id)
    if mode_id:
        message = messages.build_mode_is_set_message(mode_id)
        await enable_mode(user, mode_id)
        return await settings(update, context, message=message)


async def back(update, context):
    """Кнопка назад."""
    user = await get_user_or_raise(update.effective_user.id)
    await update.message.reply_text(
        messages.MAIN_MENU_MESSAGE, reply_markup=get_start_keyboard(user)
    )
    return ConversationHandler.END


async def stopping_decline(update, context):
    return await back_to_settings(
        update, context, message=messages.PROGRAM_STOPPING_CANCELED_MESSAGE
    )


def register_handlers(application):
    application.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(
                    filters=button(SETTINGS_BUTTON_TEXT),
                    callback=settings,
                )
            ],
            states={
                SETTINGS: [
                    MessageHandler(
                        button(START_PROGRAM_BUTTON_TEXT),
                        start_program
                    ),
                    MessageHandler(
                        button(INTERVALS_BUTTON_TEXT),
                        show_intervals
                    ),
                    MessageHandler(
                        button(STOP_PROGRAM_BUTTON_TEXT),
                        stop_program
                    ),
                    MessageHandler(
                        button(SWITCH_MODE_BUTTON_TEXT),
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
                        button(APPLY_STOP_BUTTON_TEXT),
                        stopping_apply
                    ),
                    MessageHandler(
                        button(CANCEL_STOP_BUTTON_TEXT),
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

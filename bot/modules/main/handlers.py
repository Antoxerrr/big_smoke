from telegram.constants import ParseMode
from telegram.ext import CommandHandler, MessageHandler
from tortoise import timezone

from bot.core.exceptions import DateSmokedGreaterThanToday
from bot.core.filters import button
from bot.core.helpers import get_user_or_raise
from bot.modules.main import messages
from bot.modules.main.helpers import get_or_create_user, beautiful_smoke_ask_answer
from bot.modules.main.keyboards import (
    get_start_keyboard, CAN_I_SMOKE_BUTTON_TEXT, I_SMOKED_BUTTON_TEXT
)
from bot.smoking.calculator import SmokingTimeCalculator


async def start(update, context):
    """Обработчик команды start."""
    user = await get_or_create_user(update.effective_user)
    keyboard = get_start_keyboard(user)
    await update.message.reply_text(
        messages.HELLO_START_MESSAGE,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )


def check_user_last_smoke_date(user):
    if user.last_smoked and user.last_smoked > timezone.now():
        exception = DateSmokedGreaterThanToday()
        raise exception


async def smoke_asking(update, context):
    """Обработка кнопки 'Можно курить?'."""
    user = await get_user_or_raise(update.effective_user.id)
    if user.program_is_active:
        check_user_last_smoke_date(user)
        next_smoke_time, smoking_allowed = await SmokingTimeCalculator.calculate(
            user
        )
        if smoking_allowed:
            await update.message.reply_text(messages.YOU_CAN_SMOKE_MESSAGE)
        else:
            answer = beautiful_smoke_ask_answer(next_smoke_time)
            await update.message.reply_text(
                answer, parse_mode=ParseMode.MARKDOWN
            )


async def smoke_update(update, context):
    """Обработка кнопки 'Я покурил'."""
    user = await get_user_or_raise(update.effective_user.id)
    if user.program_is_active:
        user.last_smoked = timezone.now()
        await user.save()
        await update.message.reply_text(messages.TIMER_IS_UPDATED_MESSAGE)


async def on_error(update, context):
    """Обработчик ошибок."""
    error_msg = str(context.error)
    message = (
        f'{messages.AN_ERROR_OCCURRED_MESSAGE} \n\n `{error_msg}`'
    )
    effective_message = update.effective_message if update else None
    if effective_message:
        await effective_message.reply_text(
            message, parse_mode=ParseMode.MARKDOWN
        )


async def help_cmd(update, context):
    """Обработчик команды /help."""
    await update.message.reply_text(
        messages.HELP_TEXT, parse_mode=ParseMode.MARKDOWN
    )


def register_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_cmd))
    application.add_handler(
        MessageHandler(
            button(CAN_I_SMOKE_BUTTON_TEXT),
            smoke_asking
        )
    )
    application.add_handler(
        MessageHandler(
            button(I_SMOKED_BUTTON_TEXT),
            smoke_update
        )
    )
    application.add_error_handler(on_error)

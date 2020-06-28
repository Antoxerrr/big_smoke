import os

from telegram.ext import Updater

from core.exceptions import TokenNotSpecifiedException

TOKEN: str = os.getenv('TOKEN')
if not TOKEN:
    raise TokenNotSpecifiedException()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

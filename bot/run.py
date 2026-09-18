import logging
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from bot.db.config import init_db
from bot.core.exceptions import TokenNotSpecifiedException
from bot.modules.main.handlers import register_handlers as register_main_handlers
from bot.modules.settings.handlers import register_handlers as register_settings_handlers

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def on_startup(application):
    await init_db()


def get_proxy_url():
    host = os.getenv('PROXY_HOST')
    if not host:
        return None
    port = os.getenv('PROXY_PORT', '1081')
    user = os.getenv('PROXY_USER')
    password = os.getenv('PROXY_PASSWORD')
    auth = f'{user}:{password}@' if user and password else ''
    return f'socks5://{auth}{host}:{port}'


def main():
    token = os.getenv('TOKEN')
    if not token:
        raise TokenNotSpecifiedException()

    builder = ApplicationBuilder().token(token).post_init(on_startup)

    proxy_url = get_proxy_url()
    if proxy_url:
        builder = builder.proxy(proxy_url).get_updates_proxy(proxy_url)

    application = builder.build()
    register_main_handlers(application)
    register_settings_handlers(application)

    application.run_polling()


if __name__ == '__main__':
    main()

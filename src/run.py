import logging
import os

import sentry_sdk

from core.db.setup import db_connection
from core.loader import PackagesLoader
from core.telegram import updater
from settings import MODULES

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def load_modules():
    loader = PackagesLoader()
    packages = [f'modules.{item}' for item in MODULES]
    loader.load_packages(packages)


def main():
    sentry_dsn = os.getenv('SENTRY_DSN', None)
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn)

    load_modules()
    connection = db_connection()  # noqa
    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()

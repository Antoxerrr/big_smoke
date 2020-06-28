import logging

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
    load_modules()
    connection = db_connection()
    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()

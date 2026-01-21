import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_NAME = os.getenv('POSTGRES_NAME')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

postgres_dsn = (
    f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
)


TORTOISE_CONFIG = {
    'use_tz': True,
    'timezone': 'Asia/Vladivostok',
    'connections': {'default': postgres_dsn},
    'apps': {
        'models': {
            'models': [
                'aerich.models',
                'bot.db.models',
            ],
            'default_connection': 'default',
        },
    },
}


async def init_db():
    await Tortoise.init(TORTOISE_CONFIG)

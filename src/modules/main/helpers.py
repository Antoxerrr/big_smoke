from mongoengine import DoesNotExist
from telegram import User as TelegramUser

from core.db.models import User


def get_or_create_user(telegram_user: TelegramUser) -> User:
    try:
        user = User.objects.get(user_id=telegram_user.id)
    except DoesNotExist:
        user = User(
            user_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
        ).save()
    else:
        user.username = telegram_user.username
        user.first_name = telegram_user.first_name
        user.last_name = telegram_user.last_name
        user.save()

    return user

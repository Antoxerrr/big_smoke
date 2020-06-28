class TokenNotSpecifiedException(Exception):
    """Исключение в случае не указанного токена бота."""

    def __str__(self):
        return 'Не указан токен телеграм бота.'


class UserNotFoundUnexpectedError(Exception):
    """Исключение - юзер не найден.

    Должно вызываться во время работы программы если юзер не найден тогда,
    когда по идее должен был быть найден. :P
    """

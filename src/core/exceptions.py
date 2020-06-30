class TokenNotSpecifiedException(Exception):
    """Исключение в случае не указанного токена бота."""

    def __str__(self):
        return 'Bot token is not specified.'


class UserNotFoundUnexpectedError(Exception):
    """Исключение - юзер не найден.

    Должно вызываться во время работы программы если юзер не найден тогда,
    когда по идее должен был быть найден. :P
    """

    def __str__(self):
        return 'User that is using bot was not found in database.'


class DateSmokedGreaterThanToday(Exception):

    def __str__(self):
        return 'Last smoking date for some reason is greater than now.'

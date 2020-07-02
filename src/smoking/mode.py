from datetime import datetime, timedelta


# Ебаный костыль
DEFAULT_SMOKING_INTERVAL = timedelta(minutes=20)


class BaseMode:
    """Базовый класс режима.

    Режим определяет насколько сильным будет прирост
    интервала курения ежедневно и умеет вычислять этот самый интервал.
    """

    # Название режима
    name: str
    # Идентификатор режима
    mode_id: int

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        """Основной метод.

        Определяет функцию, которая вычисляет интервал курения
        для текущего дня.
        """
        raise NotImplementedError()

    @classmethod
    def get_interval(
            cls, date_start: datetime, date_end: datetime = None
    ) -> timedelta:
        """Вычисляет время, когда можно в следующий раз покурить."""
        if not date_end:
            date_end = datetime.now()
        days_delta = (date_end - date_start).days
        if days_delta <= 0:
            smoking_interval = timedelta()
        else:
            smoking_interval = timedelta(
                hours=cls.calculate_interval(days_delta)
            )
        return smoking_interval


class EasyMode(BaseMode):
    """Лёгкий режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~4 часа 20 минут
    """

    name = 'Лёгкий'
    mode_id = 1

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return (days_delta / 2.5) - (days_delta / 3.7) + 0.3


class NormalMode(BaseMode):
    """Обычный режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~7 часов 10 минут
    """

    name = 'Обычный'
    mode_id = 2

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return days_delta / 4.44 + 0.2


class HardMode(BaseMode):
    """Сложный режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~13 часов 10 минут
    """

    name = 'Сложный'
    mode_id = 3

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return (days_delta / 4.44) + (0.2 * days_delta)

from datetime import datetime, timedelta


class BaseMode:
    """Базовый класс режима.

    Режим определяет насколько сильным будет прирост
    интервала курения ежедневно и умеет вычислять этот самый интервал.
    """

    # Название режима
    name: str

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        """Основной метод.

        Определяет функцию, которая вычисляет интервал курения
        для текущего дня.
        """
        raise NotImplementedError()

    @classmethod
    def ask_for_smoke(
        cls, date_start: datetime, date_last_smoked: datetime
    ) -> (datetime, bool):
        """Вычисляет время, когда можно в следующий раз покурить."""
        # Прибавляем к делье единицу, включая последний день в дельту
        days_delta = (datetime.now() - date_start).days + 1
        smoking_interval = timedelta(hours=cls.calculate_interval(days_delta))

        next_smoke_time = date_last_smoked + smoking_interval
        smoking_allowed = next_smoke_time < datetime.now()
        return next_smoke_time, smoking_allowed


class EasyMode(BaseMode):
    """Лёгкий режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~4 часа 20 минут
    """

    name = 'Лёгкий'

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return (days_delta / 2.5) - (days_delta / 3.7) + 0.3


class NormalMode(BaseMode):
    """Обычный режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~7 часов 10 минут
    """

    name = 'Обычный'

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return days_delta / 4.44 + 0.2


class HardMode(BaseMode):
    """Сложный режим.

    Интервал в первый день ~25 минут
    Интервал через месяц ~13 часов 10 минут
    """

    name = 'Сложный'

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        return (days_delta / 4.44) + (0.2 * days_delta)

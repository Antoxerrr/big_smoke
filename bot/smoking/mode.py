from datetime import datetime, timedelta
import math

from tortoise import timezone


# Ебаный костыль
DEFAULT_SMOKING_INTERVAL = timedelta(minutes=20)


class BaseMode:
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
            date_end = timezone.now()
        days_delta = (date_end - date_start).days
        day_number = max(1, days_delta + 1)
        return timedelta(hours=cls.calculate_interval(day_number))


class EasyMode(BaseMode):
    name = 'Лёгкий'
    mode_id = 1

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        start = 20 / 60
        day7 = 30 / 60
        day14 = 1.0
        day30 = 2.0
        if days_delta <= 1:
            return start
        if days_delta <= 14:
            t = (days_delta - 1) / 13
            p = math.log((day7 - start) / (day14 - start), 6 / 13)
            return start + (day14 - start) * (t ** p)
        return day14 + (day30 - day14) * ((days_delta - 14) / 16)


class NormalMode(BaseMode):
    name = 'Обычный'
    mode_id = 2

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        start = 25 / 60
        day7 = 45 / 60
        day14 = 1.0
        day30 = 2.5
        if days_delta <= 1:
            return start
        if days_delta <= 14:
            t = (days_delta - 1) / 13
            p = math.log((day7 - start) / (day14 - start), 6 / 13)
            return start + (day14 - start) * (t ** p)
        return day14 + (day30 - day14) * ((days_delta - 14) / 16)


class HardMode(BaseMode):
    name = 'Сложный'
    mode_id = 3

    @classmethod
    def calculate_interval(cls, days_delta: int) -> float:
        start = 30 / 60
        day7 = 1.0
        day14 = 2.0
        day30 = 4.0
        if days_delta <= 1:
            return start
        if days_delta <= 14:
            t = (days_delta - 1) / 13
            p = math.log((day7 - start) / (day14 - start), 6 / 13)
            return start + (day14 - start) * (t ** p)
        return day14 + (day30 - day14) * ((days_delta - 14) / 16)

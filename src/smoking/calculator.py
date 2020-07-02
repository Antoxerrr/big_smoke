from datetime import datetime, timedelta
from typing import List

from core.db.models import User, ModeUsage
from smoking.mode import DEFAULT_SMOKING_INTERVAL
from smoking.modes_map import modes_map


class SmokingTimeCalculator:
    """Вычисляет, когда можно юзеру покурить."""

    mode_usages_pipeline = [
        {
            '$group': {
                '_id': '$mode_id',
                'dates': {
                    '$push': {'date_start': '$date_start',
                              'date_end': '$date_end'}
                }
            }
        }
    ]

    @classmethod
    def calculate(cls, user: User) -> (datetime, bool):
        """Основной метод."""
        grouped_mode_usages = cls._get_grouped_mode_usages(user)
        next_smoke_time = cls._get_next_smoke_time(user, grouped_mode_usages)
        smoking_allowed = next_smoke_time < datetime.now()
        return next_smoke_time, smoking_allowed

    @classmethod
    def _get_grouped_mode_usages(cls, user: User) -> list:
        return list(
            ModeUsage.objects(user=user).aggregate(cls.mode_usages_pipeline)
        )

    @staticmethod
    def _get_mode(mode_id):
        mode = modes_map.get(mode_id)
        if not mode:
            raise Exception('Ошибка получения текущего режима работы.')
        return mode

    @classmethod
    def _get_next_smoke_time(
            cls, user: User, mode_usages: List[dict]
    ) -> datetime:
        total_delta = cls._total_delta(mode_usages)
        if total_delta.total_seconds() == 0:
            total_delta = DEFAULT_SMOKING_INTERVAL
        return user.last_smoked + total_delta

    @classmethod
    def _total_delta(cls, mode_usages: List[dict]) -> timedelta:
        return sum(
            [cls._get_usage_delta(usage) for usage in mode_usages],
            timedelta()
        )

    @classmethod
    def _get_usage_delta(cls, usage: dict) -> timedelta:
        dates_list = usage.get('dates')
        mode = cls._get_mode(usage.get('_id'))
        return sum(
            [mode.get_interval(**dates) for dates in dates_list],
            timedelta()
        )

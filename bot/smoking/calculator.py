from datetime import datetime, timedelta

from tortoise import timezone
from typing import Dict, List

from bot.db.models import User, ModeUsage
from bot.smoking.mode import DEFAULT_SMOKING_INTERVAL
from bot.smoking.modes_map import modes_map


class SmokingTimeCalculator:
    """Вычисляет, когда можно юзеру покурить."""

    @classmethod
    async def calculate(cls, user: User) -> tuple[datetime, bool]:
        """Основной метод."""
        grouped_mode_usages = await cls._get_grouped_mode_usages(user)
        next_smoke_time = cls._get_next_smoke_time(user, grouped_mode_usages)
        smoking_allowed = next_smoke_time < timezone.now()
        return next_smoke_time, smoking_allowed

    @classmethod
    async def _get_grouped_mode_usages(cls, user: User) -> list:
        usages = await ModeUsage.filter(user=user).values(
            'mode_id', 'date_start', 'date_end'
        )
        grouped: Dict[int, Dict[str, list]] = {}
        for usage in usages:
            mode_id = usage['mode_id']
            grouped.setdefault(mode_id, {'_id': mode_id, 'dates': []})
            grouped[mode_id]['dates'].append({
                'date_start': usage['date_start'],
                'date_end': usage['date_end'],
            })
        return list(grouped.values())

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

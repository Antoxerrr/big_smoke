from bot.db.models import User, ModeUsage


async def get_user_mode_id(user: User):
    usage: ModeUsage = await ModeUsage.filter(
        date_end=None, user=user
    ).first()
    if not usage:
        return None
    return usage.mode_id

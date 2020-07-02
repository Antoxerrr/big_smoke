from core.db.models import User, ModeUsage


def get_user_mode_id(user: User):
    usage: ModeUsage = ModeUsage.objects(date_end=None, user=user).first()
    if not usage:
        return None
    return usage.mode_id

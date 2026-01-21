from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(primary_key=True)
    program_is_active = fields.BooleanField(default=False)
    last_smoked = fields.DatetimeField(null=True)


class ModeUsage(Model):
    user = fields.ForeignKeyField('models.User', related_name='mode_usages')
    mode_id = fields.IntField()
    date_start = fields.DatetimeField()
    date_end = fields.DatetimeField(null=True)

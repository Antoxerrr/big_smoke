from mongoengine import Document, fields, CASCADE


class User(Document):

    # Базовые поля пользователя телеграма
    user_id = fields.IntField(required=True, unique=True)
    username = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()

    # Флаг запущена ли программа бота у юзера
    program_is_active = fields.BooleanField(default=False)
    # Когда последний раз покурил
    last_smoked = fields.DateTimeField()


class ModeUsage(Document):
    """Модель 'Использование режима'."""

    user = fields.ReferenceField(
        User, reverse_delete_rule=CASCADE, required=True
    )
    mode_id = fields.IntField(required=True)
    date_start = fields.DateTimeField(required=True)
    date_end = fields.DateTimeField(required=False)

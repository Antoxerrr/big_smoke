from mongoengine import Document, fields


class User(Document):

    # Базовые поля пользователя телеграма
    user_id = fields.IntField(required=True, unique=True)
    username = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()

    # Основые поля
    # Начало работы по программе бота
    date_start = fields.DateTimeField()
    # Когда последний раз покурил
    last_smoked = fields.DateTimeField()
    # Идентификатор режима работы
    mode_id = fields.IntField()

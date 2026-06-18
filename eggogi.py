class ValueUnacceptableError(Exception):
    """Ошибка: недопустимое значение"""
    pass


class FieldNotFoundError(Exception):
    """Ошибка: обращение к несуществующему полю таблицы"""
    pass

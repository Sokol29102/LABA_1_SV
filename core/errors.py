#core/errors.py
from __future__ import annotations


class ValidationError(Exception):
    #помилка при перевірці значень типів або рядків
    pass


class SchemaError(Exception):
    #помилка структури таблиці або схеми
    pass


class StorageError(Exception):
    #помилка збереження або читання з диску
    pass


class DatabaseError(Exception):
    #загальна помилка бази даних
    pass

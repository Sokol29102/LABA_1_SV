# core/types_base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Type(ABC):
#базовий абстрактний тип поля таблиці
#відповідає за парсинг, валідацію та серіалізацію значення


    def __init__(self, name: str) -> None:
        # логічна назва типу, наприклад "integer", "complexReal"
        self.name = name

    @abstractmethod
    def parse(self, raw: Any) -> Any:
#парсить сире значення з вводу користувача або json
#кидає ValueError при невдалому парсингу

        raise NotImplementedError

    @abstractmethod
    def validate(self, value: Any) -> bool:
#перевіряє, що значення відповідає цьому типу
#повертає True/False, може кинути ValueError для деталі

        raise NotImplementedError

    @abstractmethod
    def serialize(self, value: Any) -> Any:
#готує значення до збереження в json
#в нормі повертає прості типи: int, float, str, dict

        raise NotImplementedError

    def parse_and_validate(self, raw: Any) -> Any:
#зручний метод: parse + validate в одному місці

        value = self.parse(raw)
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid for type {self.name}")
        return value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


class TypeRegistry:
#простий реєстр типів за ім'ям, щоб можна було будувати схему з рядків


    def __init__(self) -> None:
        self._types: dict[str, Type] = {}

    def register(self, t: Type) -> None:
        #реєструє екземпляр типу під його ім'ям
        key = t.name
        if key in self._types:
            raise ValueError(f"type {key!r} already registered")
        self._types[key] = t

    def get(self, name: str) -> Type:
        #повертає тип за ім'ям
        try:
            return self._types[name]
        except KeyError as exc:
            raise KeyError(f"unknown type {name!r}") from exc

    def has(self, name: str) -> bool:
        #перевіряє, чи існує тип
        return name in self._types

    def available_types(self) -> list[str]:
        #повертає список імен доступних типів
        return sorted(self._types.keys())


#глобальний реєстр, яким користуватиметься вся система
global_type_registry = TypeRegistry()

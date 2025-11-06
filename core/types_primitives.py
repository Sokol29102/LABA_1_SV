# core/types_primitives.py
from __future__ import annotations

from typing import Any

from .types_base import Type, global_type_registry


class IntegerType(Type):
    """
    тип для цілих чисел
    """

    def __init__(self) -> None:
        super().__init__(name="integer")

    def parse(self, raw: Any) -> int:
        # пробує перетворити сире значення до int
        if raw is None:
            raise ValueError("integer value cannot be None")
        if isinstance(raw, bool):
            # не хочемо трактувати bool як int
            raise ValueError("bool is not valid integer")
        if isinstance(raw, int):
            return raw
        try:
            return int(str(raw).strip())
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as integer") from exc

    def validate(self, value: Any) -> bool:
        # перевіряє що значення є int (не bool)
        return isinstance(value, int) and not isinstance(value, bool)

    def serialize(self, value: Any) -> int:
        # для json достатньо мати int
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid integer")
        return int(value)


class RealType(Type):
    """
    тип для дійсних чисел
    """

    def __init__(self) -> None:
        super().__init__(name="real")

    def parse(self, raw: Any) -> float:
        # пробує перетворити сире значення до float
        if raw is None:
            raise ValueError("real value cannot be None")
        if isinstance(raw, (int, float)) and not isinstance(raw, bool):
            return float(raw)
        try:
            return float(str(raw).strip().replace(",", "."))
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as real") from exc

    def validate(self, value: Any) -> bool:
        # перевіряє що значення є числом (int або float, але не bool)
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def serialize(self, value: Any) -> float:
        # для json достатньо мати float
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid real")
        return float(value)


class CharType(Type):
    """
    тип для одного символу
    """

    def __init__(self) -> None:
        super().__init__(name="char")

    def parse(self, raw: Any) -> str:
        # приводить значення до рядка і бере перший символ
        if raw is None:
            raise ValueError("char value cannot be None")
        s = str(raw)
        if len(s) == 0:
            raise ValueError("char value cannot be empty")
        return s[0]

    def validate(self, value: Any) -> bool:
        # перевіряє що значення є рядком довжини 1
        return isinstance(value, str) and len(value) == 1

    def serialize(self, value: Any) -> str:
        # в json зберігаємо як рядок довжини 1
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid char")
        return value


class StringType(Type):
    """
    тип для довільного рядка
    """

    def __init__(self) -> None:
        super().__init__(name="string")

    def parse(self, raw: Any) -> str:
        # просто перетворює значення на рядок
        if raw is None:
            return ""
        return str(raw)

    def validate(self, value: Any) -> bool:
        # перевіряє що значення є рядком
        return isinstance(value, str)

    def serialize(self, value: Any) -> str:
        # в json зберігаємо як рядок
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid string")
        return value


def register_builtin_types() -> None:
    """
    реєструє базові типи в глобальному реєстрі
    викликається один раз при старті програми
    """
    for t in (IntegerType(), RealType(), CharType(), StringType()):
        if not global_type_registry.has(t.name):
            global_type_registry.register(t)


# реєструємо типи одразу при імпорті модуля
register_builtin_types()

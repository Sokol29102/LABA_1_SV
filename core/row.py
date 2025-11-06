# core/row.py
from __future__ import annotations

from typing import Any, Dict


class Row:
    #один рядок таблиці
    #зберігає значення як словник поле -> значення вже після валідації


    def __init__(self, values: Dict[str, Any]) -> None:
        #тут припускаємо, що значення вже провалідовані схемою
        self._values: Dict[str, Any] = dict(values)

    def get(self, field_name: str) -> Any:
        #повертає значення поля по імені
        return self._values[field_name]

    def set(self, field_name: str, value: Any) -> None:
        #змінює значення поля
        self._values[field_name] = value

    def as_dict(self) -> Dict[str, Any]:
        #повертає копію словника значень
        return dict(self._values)

    def items(self):
        #ітерується по парах (ім'я поля, значення)
        return self._values.items()

    def __getitem__(self, key: str) -> Any:
        #дозволяє row["field"] синтаксис
        return self._values[key]

    def __setitem__(self, key: str, value: Any) -> None:
        #дозволяє row["field"] = value
        self._values[key] = value

    def __repr__(self) -> str:
        return f"Row({self._values!r})"

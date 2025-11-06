# core/table.py
from __future__ import annotations

from typing import Any, List

from .schema import Schema
from .row import Row


class Table:
    #таблиця бази даних, що має схему та список рядків


    def __init__(self, name: str, schema: Schema) -> None:
        self.name = name
        self.schema = schema
        self.rows: List[Row] = []
        self.is_dirty: bool = False #прапорець змін
        self.loaded: bool = True #позначає що таблиця існує в пам’яті

    def insert(self, data: dict[str, Any]) -> Row:
        #додає новий рядок після перевірки
        normalized = self.schema.validate_row(data)
        row = Row(normalized)
        self.rows.append(row)
        self.is_dirty = True
        return row

    def update(self, index: int, new_data: dict[str, Any]) -> None:
        #змінює рядок за індексом
        if not (0 <= index < len(self.rows)):
            raise IndexError("row index out of range")
        normalized = self.schema.validate_row(new_data)
        self.rows[index] = Row(normalized)
        self.is_dirty = True

    def delete(self, index: int) -> None:
        #видаляє рядок
        if not (0 <= index < len(self.rows)):
            raise IndexError("row index out of range")
        self.rows.pop(index)
        self.is_dirty = True

    def get_rows(self) -> list[Row]:
        #повертає список усіх рядків
        return list(self.rows)

    def row_count(self) -> int:
        #кількість рядків
        return len(self.rows)

    def as_serializable(self) -> list[dict[str, Any]]:
        #повертає серіалізований список рядків для json
        return [self.schema.serialize_row(r.as_dict()) for r in self.rows]

    def mark_saved(self) -> None:
        #скидає прапорець змін після збереження
        self.is_dirty = False

    def __repr__(self) -> str:
        return f"Table(name={self.name!r}, rows={len(self.rows)})"

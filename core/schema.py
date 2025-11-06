# core/schema.py
from __future__ import annotations

from typing import Any

from .types_base import Type, global_type_registry


class Field:
    #опис одного поля таблиці

    def __init__(self, name: str, type_name: str) -> None:
        self.name = name.strip()
        if not global_type_registry.has(type_name):
            raise ValueError(f"unknown type {type_name!r}")
        self.type_name = type_name
        self.type_obj: Type = global_type_registry.get(type_name)

    def validate_value(self, raw_value: Any) -> Any:
        #парсить і перевіряє значення відповідно до типу
        return self.type_obj.parse_and_validate(raw_value)

    def serialize_value(self, value: Any) -> Any:
        #готує значення до json
        return self.type_obj.serialize(value)

    def as_dict(self) -> dict[str, Any]:
        #повертає словник для збереження схеми
        return {"name": self.name, "type": self.type_name}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Field":
        #створює поле з json-опису
        return Field(name=data["name"], type_name=data["type"])

    def __repr__(self) -> str:
        return f"Field({self.name!r}, {self.type_name!r})"


class Schema:
    #опис структури таблиці (набір полів)

    def __init__(self, fields: list[Field]) -> None:
        if not fields:
            raise ValueError("schema must contain at least one field")
        names = [f.name for f in fields]
        if len(names) != len(set(names)):
            raise ValueError("duplicate field names in schema")
        self.fields = fields
        self._name_to_field = {f.name: f for f in fields}

    def field_names(self) -> list[str]:
        #повертає список назв полів
        return [f.name for f in self.fields]

    def validate_row(self, row_data: dict[str, Any]) -> dict[str, Any]:
        #перевіряє та нормалізує значення рядка згідно схеми
        #повертає новий словник зі скоригованими значеннями

        result = {}
        for field in self.fields:
            if field.name not in row_data:
                raise ValueError(f"missing field {field.name!r} in row data")
            value = row_data[field.name]
            result[field.name] = field.validate_value(value)
        return result

    def serialize_row(self, row_data: dict[str, Any]) -> dict[str, Any]:
        #перетворює значення рядка для збереження в json
        result = {}
        for field in self.fields:
            result[field.name] = field.serialize_value(row_data[field.name])
        return result

    def as_dict(self) -> dict[str, Any]:
        #повертає словник для збереження схеми
        return {"fields": [f.as_dict() for f in self.fields]}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Schema":
        #відновлює схему з json
        fields = [Field.from_dict(fd) for fd in data["fields"]]
        return Schema(fields)

    def __repr__(self) -> str:
        parts = ", ".join(f"{f.name}:{f.type_name}" for f in self.fields)
        return f"Schema({parts})"

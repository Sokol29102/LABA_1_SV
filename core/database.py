# core/database.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .table import Table
from .schema import Schema
from .row import Row
from storage.file_storage import save_table, load_table


class Database:
    #базовий клас для роботи з табличною базою даних


    def __init__(self, name: str, base_dir: str = "db_data") -> None:
        self.name = name
        self.base_path = Path(base_dir) / name
        self.tables: dict[str, Table] = {}

        #створюємо папку якщо її немає
        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_table(self, name: str, schema: Schema) -> Table:
        #створює нову таблицю і додає її до бази
        if name in self.tables:
            raise ValueError(f"table {name!r} already exists")
        table = Table(name=name, schema=schema)
        self.tables[name] = table
        return table

    def drop_table(self, name: str) -> None:
        #видаляє таблицю з бази (файл лишається)
        if name not in self.tables:
            raise KeyError(f"table {name!r} not found")
        del self.tables[name]

    def get_table(self, name: str) -> Table:
        #повертає таблицю за ім'ям
        if name not in self.tables:
            raise KeyError(f"table {name!r} not found")
        return self.tables[name]

    def list_tables(self) -> list[str]:
        #повертає список назв таблиць
        return sorted(self.tables.keys())

    def save_all(self) -> None:
        #зберігає усі таблиці в сховище
        for table in self.tables.values():
            save_table(table, base_path=self.base_path)
            table.mark_saved()

        #записуємо мета-файл з переліком таблиць
        meta = {"tables": list(self.tables.keys())}
        meta_path = self.base_path / "db_meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    def load_all(self) -> None:
        #завантажує всі таблиці з диску (якщо є)
        meta_path = self.base_path / "db_meta.json"
        if not meta_path.exists():
            return

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        for tname in meta.get("tables", []):
            table = load_table(tname, base_path=self.base_path)
            self.tables[tname] = table

    def __repr__(self) -> str:
        return f"Database(name={self.name!r}, tables={list(self.tables.keys())})"

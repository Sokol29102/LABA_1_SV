# storage/file_storage.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.table import Table
from core.schema import Schema
from core.row import Row


def _tables_dir(base_path: Path) -> Path:
    #повертає шлях до папки з таблицями для цієї бази
    tables_path = base_path / "tables"
    tables_path.mkdir(parents=True, exist_ok=True)
    return tables_path


def save_table(table: Table, base_path: Path) -> None:
    #зберігає одну таблицю:
    #- схему в <name>.schema.json
    #- рядки в <name>.rows.jsonl

    tables_path = _tables_dir(base_path)
    schema_path = tables_path / f"{table.name}.schema.json"
    rows_path = tables_path / f"{table.name}.rows.jsonl"

    #зберігаємо схему
    schema_dict = table.schema.as_dict()
    with open(schema_path, "w", encoding="utf-8") as f:
        json.dump(schema_dict, f, indent=2, ensure_ascii=False)

    #зберігаємо рядки у форматі jsonl
    with open(rows_path, "w", encoding="utf-8") as f:
        for row in table.rows:
            serialized = table.schema.serialize_row(row.as_dict())
            f.write(json.dumps(serialized, ensure_ascii=False))
            f.write("\n")


def load_table(name: str, base_path: Path) -> Table:

    #завантажує таблицю з диску за ім'ям
    #очікує:
    #- <name>.schema.json
    #- <name>.rows.jsonl (може бути відсутній або порожній)
    tables_path = _tables_dir(base_path)
    schema_path = tables_path / f"{name}.schema.json"
    rows_path = tables_path / f"{name}.rows.jsonl"

    if not schema_path.exists():
        raise FileNotFoundError(f"schema file for table {name!r} not found")

    #читаємо схему
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_data = json.load(f)
    schema = Schema.from_dict(schema_data)

    table = Table(name=name, schema=schema)

    #читаємо рядки, якщо файл існує
    if rows_path.exists():
        with open(rows_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                raw_row: dict[str, Any] = json.loads(line)
                # пропускаємо через валідацію, щоб відновити потрібні типи
                normalized = schema.validate_row(raw_row)
                table.rows.append(Row(normalized))

    table.is_dirty = False
    return table

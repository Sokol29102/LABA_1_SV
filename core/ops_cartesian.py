# core/ops_cartesian.py
from __future__ import annotations

from typing import Any

from .table import Table
from .schema import Schema, Field
from .row import Row


def _prefixed_fields(schema: Schema, prefix: str) -> list[Field]:
    #створює новий список полів з доданим префіксом до імен

    new_fields: list[Field] = []
    for f in schema.fields:
        new_name = f"{prefix}{f.name}"
        new_fields.append(Field(name=new_name, type_name=f.type_name))
    return new_fields


def cartesian_product(table_a: Table, table_b: Table, result_name: str | None = None) -> Table:
    #виконує декартів добуток двох таблиць:
    #результат містить усі комбінації рядків (a, b), де a з A, b з B
    #схема результату: поля A_* для таблиці A, поля B_* для таблиці B

    if table_a.row_count() == 0 or table_b.row_count() == 0:
        #результат порожній, але схема все одно є важливою
        pass

    #будуємо схему результату
    fields_a = _prefixed_fields(table_a.schema, "A_")
    fields_b = _prefixed_fields(table_b.schema, "B_")
    result_schema = Schema(fields=fields_a + fields_b)

    if result_name is None:
        result_name = f"{table_a.name}_x_{table_b.name}"

    result_table = Table(name=result_name, schema=result_schema)

    #обходимо всі пари рядків
    for row_a in table_a.get_rows():
        for row_b in table_b.get_rows():
            data: dict[str, Any] = {}
            #додаємо значення з таблиці A
            for field in table_a.schema.fields:
                data[f"A_{field.name}"] = row_a.get(field.name)
            #додаємо значення з таблиці B
            for field in table_b.schema.fields:
                data[f"B_{field.name}"] = row_b.get(field.name)

            #вставляємо рядок без додаткової валідації, бо ми вже узгодили схему
            normalized = result_schema.validate_row(data)
            result_table.rows.append(Row(normalized))

    #результат вважаємо новою таблицею у пам'яті, поки що позначимо як dirty
    result_table.is_dirty = True
    return result_table

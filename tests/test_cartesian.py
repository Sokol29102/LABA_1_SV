# tests/test_cartesian.py
from __future__ import annotations

from core.schema import Field, Schema
from core.table import Table
from core.ops_cartesian import cartesian_product


def _make_table_a() -> Table:
    #таблиця A(id: integer, name: string)
    schema = Schema(
        [
            Field("id", "integer"),
            Field("name", "string"),
        ]
    )
    t = Table("A", schema)
    t.insert({"id": 1, "name": "Alice"})
    t.insert({"id": 2, "name": "Bob"})
    return t


def _make_table_b() -> Table:
    #таблиця B(score: real, flag: char)
    schema = Schema(
        [
            Field("score", "real"),
            Field("flag", "char"),
        ]
    )
    t = Table("B", schema)
    t.insert({"score": 10.0, "flag": "X"})
    t.insert({"score": 20.5, "flag": "Y"})
    t.insert({"score": 30.0, "flag": "Z"})
    return t


def test_cartesian_row_count_and_schema() -> None:
    a = _make_table_a()
    b = _make_table_b()

    result = cartesian_product(a, b, result_name="A_x_B")

    #тут буде |A| * |B| = 2 * 3 = 6 рядків
    assert result.row_count() == 6

    #перевіряємо імена полів зі префіксами
    expected_fields = ["A_id", "A_name", "B_score", "B_flag"]
    assert result.schema.field_names() == expected_fields


def test_cartesian_values_are_combined_correctly() -> None:
    a = _make_table_a()
    b = _make_table_b()

    result = cartesian_product(a, b, result_name="A_x_B")

    #забираємо усі рядки як словники
    rows = [r.as_dict() for r in result.get_rows()]

    #сформуємо очікувану множину штук (A_id, A_name, B_score)
    expected = set()
    for ra in a.get_rows():
        for rb in b.get_rows():
            expected.add(
                (
                    ra["id"],
                    ra["name"],
                    rb["score"],
                )
            )

    actual = set((r["A_id"], r["A_name"], r["B_score"]) for r in rows)

    assert actual == expected

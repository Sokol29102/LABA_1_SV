# tests/test_row_validation.py
from __future__ import annotations

import pytest

from core.schema import Field, Schema
from core.row import Row


@pytest.fixture
def simple_schema() -> Schema:
    fields = [
        Field("id", "integer"),
        Field("name", "string"),
        Field("score", "real"),
    ]
    return Schema(fields)


def test_valid_row_passes(simple_schema: Schema) -> None:
    raw = {"id": 1, "name": "Alice", "score": 95.5}
    normalized = simple_schema.validate_row(raw)
    row = Row(normalized)
    assert row["id"] == 1
    assert row["name"] == "Alice"
    assert row["score"] == pytest.approx(95.5)


def test_missing_field_fails(simple_schema: Schema) -> None:
    raw = {"id": 2, "name": "Bob"}
    with pytest.raises(ValueError):
        simple_schema.validate_row(raw)


def test_type_mismatch_fails(simple_schema: Schema) -> None:
    raw = {"id": "not_int", "name": "Test", "score": 1.0}
    with pytest.raises(ValueError):
        simple_schema.validate_row(raw)

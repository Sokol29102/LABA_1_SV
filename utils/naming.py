# utils/naming.py
from __future__ import annotations


def prefixed_name(prefix: str, field_name: str) -> str:
    #повертає ім’я поля з доданим префіксом, наприклад A_id до "A_id"
    return f"{prefix}{field_name}"


def unique_name(base: str, existing: set[str]) -> str:
    #генерує унікальне ім’я, додаючи суфікс _1, _2 і т.д. якщо треба
    if base not in existing:
        return base
    i = 1
    while f"{base}_{i}" in existing:
        i += 1
    return f"{base}_{i}"

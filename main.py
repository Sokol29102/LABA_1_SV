# main.py
from __future__ import annotations

import sys
from pathlib import Path

from core.schema import Field, Schema
from core.table import Table
from core.database import Database
from core.ops_cartesian import cartesian_product


def _input_nonempty(prompt: str) -> str:
    #зчитує непорожній рядок
    while True:
        val = input(prompt).strip()
        if val:
            return val


def create_table_cli(db: Database) -> None:
    print("створення нової таблиці")
    tname = _input_nonempty("ім'я таблиці: ")
    fields: list[Field] = []

    while True:
        fname = _input_nonempty("  назва поля (або Enter для завершення): ")
        if fname == "":
            break
        ttype = _input_nonempty("  тип поля (integer, real, char, string, complexInteger, complexReal): ")
        try:
            field = Field(fname, ttype)
            fields.append(field)
        except Exception as e:
            print("  помилка:", e)
        cont = input("  додати ще поле? (y/n): ").lower()
        if cont != "y":
            break

    schema = Schema(fields)
    table = db.create_table(tname, schema)
    print(f"таблицю '{tname}' створено зі схемою: {[f.name for f in fields]}")


def add_row_cli(db: Database) -> None:
    tname = _input_nonempty("введіть ім'я таблиці: ")
    table = db.get_table(tname)
    print("додавання рядка до таблиці:", tname)
    row_data: dict[str, str] = {}
    for f in table.schema.fields:
        val = input(f"  {f.name} ({f.type_name}): ")
        row_data[f.name] = val
    try:
        table.insert(row_data)
        print("рядок додано успішно")
    except Exception as e:
        print("помилка під час додавання рядка:", e)


def show_tables_cli(db: Database) -> None:
    print("таблиці бази даних:")
    for tname in db.list_tables():
        t = db.get_table(tname)
        print(f" - {t.name} ({t.row_count()} рядків)")


def cartesian_cli(db: Database) -> None:
    print("виконання декартового добутку двох таблиць")
    a = _input_nonempty("ім'я таблиці A: ")
    b = _input_nonempty("ім'я таблиці B: ")
    if a not in db.tables or b not in db.tables:
        print("одна або обидві таблиці не знайдені")
        return
    tA = db.get_table(a)
    tB = db.get_table(b)
    result = cartesian_product(tA, tB)
    db.tables[result.name] = result
    print(f"результат '{result.name}' створено, рядків: {result.row_count()}")


def main():
    base_dir = Path("db_data")
    db_name = "default_db"
    db = Database(db_name, base_dir)
    db.load_all()

    menu = """
1. створити таблицю
2. показати таблиці
3. додати рядок
4. декартів добуток двох таблиць
5. зберегти базу
0. вихід
> """

    while True:
        choice = input(menu).strip()
        if choice == "1":
            create_table_cli(db)
        elif choice == "2":
            show_tables_cli(db)
        elif choice == "3":
            add_row_cli(db)
        elif choice == "4":
            cartesian_cli(db)
        elif choice == "5":
            db.save_all()
            print("усі таблиці збережено")
        elif choice == "0":
            db.save_all()
            print("вихід...")
            sys.exit(0)
        else:
            print("невірний вибір")


if __name__ == "__main__":
    main()

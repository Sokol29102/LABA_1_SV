# utils/cli_helpers.py
from __future__ import annotations


def print_table(data: list[dict[str, object]]) -> None:
    #просте текстове виведення таблиці у консоль
    #приймає список словників (рядки)

    if not data:
        print("(порожньо)")
        return

    #беремо порядок полів з першого рядка
    headers = list(data[0].keys())
    # бчислюємо ширину колонок
    widths = {h: max(len(str(h)), *(len(str(row[h])) for row in data)) for h in headers}

    #друкуємо заголовок
    header_line = " | ".join(f"{h:<{widths[h]}}" for h in headers)
    print(header_line)
    print("-" * len(header_line))

    #друкуємо рядки
    for row in data:
        print(" | ".join(f"{str(row[h]):<{widths[h]}}" for h in headers))


def ask_yes_no(prompt: str) -> bool:
    #просто питає 'y' або 'n'
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("введіть 'y' або 'n'")

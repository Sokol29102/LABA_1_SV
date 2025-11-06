# core/types_complex.py
from __future__ import annotations

from typing import Any, Tuple

from .types_base import Type, global_type_registry


def _parse_complex_string(raw: str) -> Tuple[float, float]:
    #допоміжна функція для парсингу рядка формату "a+bi" або "a-bi"
    #a і b можуть бути з крапкою, пробіли допускаються

    s = raw.strip().lower().replace(" ", "")
    if not s:
        raise ValueError("empty complex string")

    # якщо немає символу 'i', пробуємо інтерпретувати як дійсну частину, уявна = 0
    if "i" not in s:
        try:
            re = float(s.replace(",", "."))
            return re, 0.0
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as complex") from exc

    # прибираємо 'i' у кінці, очікуємо щось типу "a+ b" або "a-b"
    if not s.endswith("i"):
        raise ValueError(f"invalid complex format {raw!r}, expected ...i at the end")
    core = s[:-1]

    # шукаємо останній плюс або мінус не на першій позиції
    split_pos = -1
    for i in range(len(core) - 1, 0, -1):
        if core[i] in "+-":
            split_pos = i
            break

    if split_pos == -1:
        # щось типу "3i"
        try:
            im = float(core.replace(",", "."))
            return 0.0, im
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as complex") from exc

    re_str = core[:split_pos]
    im_str = core[split_pos:]

    try:
        re = float(re_str.replace(",", ".")) if re_str else 0.0
        im = float(im_str.replace(",", ".")) if im_str not in ("+", "-") else float(im_str + "1")
        return re, im
    except Exception as exc:
        raise ValueError(f"cannot parse {raw!r} as complex") from exc


class ComplexIntegerType(Type):
    """
    тип для комплексних чисел з цілими частинами (a, b), де a, b ∈ Z
    внутрішньо зберігаємо як кортеж (int, int)
    """

    def __init__(self) -> None:
        super().__init__(name="complexInteger")

    def parse(self, raw: Any) -> tuple[int, int]:
        # підтримуємо формат:
        # - (a, b) або [a, b]
        # - {"real": a, "imag": b}
        # - рядок "a+bi", "a-bi", "ai", "a"
        if raw is None:
            raise ValueError("complex integer value cannot be None")

        # вже готовий кортеж
        if isinstance(raw, tuple) and len(raw) == 2:
            re, im = raw
        elif isinstance(raw, list) and len(raw) == 2:
            re, im = raw[0], raw[1]
        elif isinstance(raw, dict) and "real" in raw and "imag" in raw:
            re, im = raw["real"], raw["imag"]
        else:
            # пробуємо парсити рядок
            re_f, im_f = _parse_complex_string(str(raw))
            re, im = int(round(re_f)), int(round(im_f))

        try:
            re_i = int(re)
            im_i = int(im)
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as complexInteger") from exc

        return re_i, im_i

    def validate(self, value: Any) -> bool:
        # перевіряємо що це кортеж з двох цілих
        if not (isinstance(value, tuple) and len(value) == 2):
            return False
        re, im = value
        return isinstance(re, int) and isinstance(im, int)

    def serialize(self, value: Any) -> dict[str, int]:
        # в json зберігаємо як {"real": a, "imag": b}
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid complexInteger")
        re, im = value
        return {"real": int(re), "imag": int(im)}


class ComplexRealType(Type):
    #тип для комплексних чисел з дійсними частинами (a, b), де a, b ∈ R
    #внутрішньо зберігаємо як кортеж (float, float)


    def __init__(self) -> None:
        super().__init__(name="complexReal")

    def parse(self, raw: Any) -> tuple[float, float]:
        #підтримуємо ті самі формати що й для цілого, але без округлення
        if raw is None:
            raise ValueError("complex real value cannot be None")

        if isinstance(raw, tuple) and len(raw) == 2:
            re, im = raw
        elif isinstance(raw, list) and len(raw) == 2:
            re, im = raw[0], raw[1]
        elif isinstance(raw, dict) and "real" in raw and "imag" in raw:
            re, im = raw["real"], raw["imag"]
        else:
            re, im = _parse_complex_string(str(raw))

        try:
            re_f = float(str(re).replace(",", "."))
            im_f = float(str(im).replace(",", "."))
        except Exception as exc:
            raise ValueError(f"cannot parse {raw!r} as complexReal") from exc

        return re_f, im_f

    def validate(self, value: Any) -> bool:
        #перевіряємо що це кортеж з двох чисел (int або float)
        if not (isinstance(value, tuple) and len(value) == 2):
            return False
        re, im = value
        return isinstance(re, (int, float)) and isinstance(im, (int, float))

    def serialize(self, value: Any) -> dict[str, float]:
        #в json зберігаємо як {"real": a, "imag": b}
        if not self.validate(value):
            raise ValueError(f"value {value!r} is not valid complexReal")
        re, im = value
        return {"real": float(re), "imag": float(im)}


def register_complex_types() -> None:

#реєструє комплексні типи в глобальному реєстрі
    for t in (ComplexIntegerType(), ComplexRealType()):
        if not global_type_registry.has(t.name):
            global_type_registry.register(t)


#реєструємо при імпорті модуля
register_complex_types()

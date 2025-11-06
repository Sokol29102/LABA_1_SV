# tests/test_types_complex.py
from __future__ import annotations

import math

import pytest

from core.types_complex import ComplexIntegerType, ComplexRealType


@pytest.fixture
def cint() -> ComplexIntegerType:
    return ComplexIntegerType()


@pytest.fixture
def creal() -> ComplexRealType:
    return ComplexRealType()


def test_complex_integer_from_tuple(cint: ComplexIntegerType) -> None:
    value = cint.parse((3, -4))
    assert value == (3, -4)
    assert cint.validate(value)
    serialized = cint.serialize(value)
    assert serialized == {"real": 3, "imag": -4}


def test_complex_integer_from_string(cint: ComplexIntegerType) -> None:
    value = cint.parse("2+5i")
    assert isinstance(value[0], int) and isinstance(value[1], int)
    assert value == (2, 5)
    serialized = cint.serialize(value)
    assert serialized == {"real": 2, "imag": 5}


def test_complex_integer_bad_value_raises(cint: ComplexIntegerType) -> None:
    with pytest.raises(ValueError):
        cint.parse("abc")


def test_complex_real_from_tuple(creal: ComplexRealType) -> None:
    value = creal.parse((1.5, -2.25))
    assert math.isclose(value[0], 1.5)
    assert math.isclose(value[1], -2.25)
    assert creal.validate(value)
    serialized = creal.serialize(value)
    assert serialized == {"real": 1.5, "imag": -2.25}


def test_complex_real_from_string(creal: ComplexRealType) -> None:
    value = creal.parse("3.2-1.8i")
    assert math.isclose(value[0], 3.2, rel_tol=1e-6)
    assert math.isclose(value[1], -1.8, rel_tol=1e-6)
    serialized = creal.serialize(value)
    assert math.isclose(serialized["real"], 3.2, rel_tol=1e-6)
    assert math.isclose(serialized["imag"], -1.8, rel_tol=1e-6)


def test_complex_real_bad_value_raises(creal: ComplexRealType) -> None:
    with pytest.raises(ValueError):
        creal.parse("i*i")

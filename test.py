from typing import Callable, Dict, List, Union, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ltlpy import (
    LTLAlways,
    LTLAnd,
    LTLEventually,
    LTLFormula,
    LTLNext,
    LTLNot,
    LTLOr,
    LTLVariable,
    ltl_interpret,
    get_variable_names,
)


def fail_get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
    pytest.fail("Unexpected function call")
    return {}


@given(st.booleans())
def test_bool(b: bool) -> None:
    f = ltl_interpret(LTLVariable(b), fail_get_lookup_table)
    assert type(f) is bool
    assert f is b


@given(st.booleans())
def test_var(b: bool) -> None:
    formula = LTLVariable("a")

    def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
        lookup_table: Dict[str, Union[bool, Callable[[], bool]]] = {"a": b}
        return lookup_table

    f = ltl_interpret(formula, get_lookup_table)
    assert type(f) is bool
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = ltl_interpret(LTLNot(LTLVariable(b)), fail_get_lookup_table)
    assert type(f) is bool
    assert f is not b


@given(st.booleans(), st.booleans())
def test_and(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLAnd(LTLVariable(b0), LTLVariable(b1)),
        fail_get_lookup_table,
    )
    assert type(f) is bool
    assert f is (b0 and b1)


@given(st.booleans(), st.booleans())
def test_or(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLOr(LTLVariable(b0), LTLVariable(b1)),
        fail_get_lookup_table,
    )
    assert type(f) is bool
    assert f is (b0 or b1)


@given(st.booleans())
def test_next(b: bool) -> None:
    f = ltl_interpret(LTLNext(LTLVariable(b)), fail_get_lookup_table)
    assert f == LTLVariable(b)


@given(st.lists(st.booleans()))
def test_eventually(lst: List[bool]) -> None:
    expected = any(lst)

    f: Union[LTLFormula, bool] = LTLEventually(LTLVariable("a"))
    for b in lst:
        if type(f) is bool:
            break

        def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
            lookup_table: Dict[str, Union[bool, Callable[[], bool]]] = {"a": b}
            return lookup_table

        f = ltl_interpret(cast(LTLFormula, f), get_lookup_table)

    if type(f) is LTLEventually:
        f = False

    assert f is expected


@given(st.lists(st.booleans()))
def test_always(lst: List[bool]) -> None:
    expected = all(lst)

    f: Union[LTLFormula, bool] = LTLAlways(LTLVariable("a"))
    for b in lst:
        if type(f) is bool:
            break

        def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
            lookup_table: Dict[str, Union[bool, Callable[[], bool]]] = {"a": b}
            return lookup_table

        f = ltl_interpret(cast(LTLFormula, f), get_lookup_table)

    if type(f) is LTLAlways:
        f = True

    assert f is expected


def test_nested_eventually_1() -> None:
    formula = LTLEventually(
        LTLAnd(
            LTLVariable("a"),
            LTLEventually(
                LTLVariable("a"),
            ),
        ),
    )

    def get_lookup_table_a_false() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False}

    def get_lookup_table_a_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": True}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    assert type(f) is bool
    assert f


def test_nested_eventually_2() -> None:
    formula = LTLEventually(
        LTLAnd(
            LTLVariable("a"),
            LTLNext(
                LTLEventually(
                    LTLVariable("a"),
                )
            ),
        ),
    )

    def get_lookup_table_a_false() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False}

    def get_lookup_table_a_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": True}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    assert type(f) is bool
    assert f


def test_nested_eventually_3() -> None:
    formula = LTLEventually(
        LTLAnd(
            LTLVariable("a"),
            LTLEventually(
                LTLVariable("b"),
            ),
        ),
    )

    def get_lookup_table_a_false() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False}

    def get_lookup_table_a_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": True}

    def get_lookup_table_b_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"b": True}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_false)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_b_true)
    assert type(f) is bool
    assert f


def test_get_variable_names() -> None:
    expected = ["a", "b"]
    formula: LTLFormula = LTLEventually(
        LTLAnd(
            LTLVariable("a"),
            LTLEventually(
                LTLVariable("b"),
            ),
        ),
    )
    actual = get_variable_names(formula)

    assert actual == expected

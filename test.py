from typing import Callable, Dict, List, Union, cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ltlpy import (
    LTLAlways,
    LTLAnd,
    LTLEventually,
    LTLFormula,
    LTLIf,
    LTLNext,
    LTLNot,
    LTLOr,
    LTLUntil,
    LTLVariable,
    get_variable_names,
    ltl_interpret,
)


def fail_get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
    pytest.fail("Unexpected function call")
    return {}


@given(st.booleans())
def test_bool(b: bool) -> None:
    f = ltl_interpret(LTLVariable(b), fail_get_lookup_table)
    assert f is b


@given(st.booleans())
def test_var(b: bool) -> None:
    formula = LTLVariable("a")

    def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
        lookup_table: Dict[str, Union[bool, Callable[[], bool]]] = {"a": b}
        return lookup_table

    f = ltl_interpret(formula, get_lookup_table)
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = ltl_interpret(LTLNot(LTLVariable(b)), fail_get_lookup_table)
    assert f is not b


@given(st.booleans(), st.booleans())
def test_and(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLAnd(LTLVariable(b0), LTLVariable(b1)),
        fail_get_lookup_table,
    )
    assert f is (b0 and b1)


@given(st.booleans(), st.booleans())
def test_or(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLOr(LTLVariable(b0), LTLVariable(b1)),
        fail_get_lookup_table,
    )
    assert f is (b0 or b1)


@given(st.booleans(), st.booleans())
def test_if(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLIf(LTLVariable(b0), LTLVariable(b1)),
        fail_get_lookup_table,
    )
    assert f is (not b0 or b1)


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


def test_eventually_with_is_final() -> None:
    formula = LTLEventually(LTLVariable("a"))
    f = ltl_interpret(formula, lambda: {"a": False}, is_final=True)
    assert f is False


def test_eventually_nested_with_is_final() -> None:
    formula = LTLEventually(LTLEventually(LTLVariable("a")))
    f = ltl_interpret(formula, lambda: {"a": False}, is_final=True)
    assert f is False


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


def test_always_with_is_final_1() -> None:
    formula = LTLAlways(LTLVariable("a"))
    f = ltl_interpret(formula, lambda: {"a": True}, is_final=True)
    assert f is True


def test_always_with_is_final_2() -> None:
    formula = LTLAlways(LTLAlways(LTLVariable("a")))
    f = ltl_interpret(formula, lambda: {"a": True}, is_final=True)
    assert f is True


def test_eventually_nested_1() -> None:
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
    assert f


def test_eventually_nested_2() -> None:
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
    assert f


def test_eventually_nested_3() -> None:
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
    assert f


def test_until_1() -> None:
    formula = LTLUntil(
        LTLVariable("a"),
        LTLVariable("b"),
    )

    def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False, "b": False}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table)
    assert not f


def test_until_2() -> None:
    formula = LTLUntil(
        LTLVariable("a"),
        LTLVariable("b"),
    )

    def get_lookup_table() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False, "b": True}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table)
    assert f


def test_until_3() -> None:
    formula = LTLUntil(
        LTLVariable("a"),
        LTLVariable("b"),
    )

    def get_lookup_table_a_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": True, "b": False}

    def get_lookup_table_b_true() -> Dict[str, Union[bool, Callable[[], bool]]]:
        return {"a": False, "b": True}

    f: Union[LTLFormula, bool] = formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_a_true)
    assert f == formula
    f = ltl_interpret(cast(LTLFormula, f), get_lookup_table_b_true)
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

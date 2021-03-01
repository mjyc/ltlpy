import pytest
from typing import cast, List, Union
from hypothesis import given, strategies as st
from ltlpy import (
    LTLFormula,
    LTLVariable,
    LTLNot,
    LTLAnd,
    LTLOr,
    LTLNext,
    LTLEventually,
    ltl_interpret,
)


@given(st.booleans())
def test_bool(b: bool) -> None:
    f = ltl_interpret(LTLVariable(b), lambda _: pytest.fail("Unexpected lookup call"))
    assert type(f) is bool
    assert f is b


@given(st.booleans())
def test_var(b: bool) -> None:
    def lookup(name: str) -> bool:
        return name == "a"

    formula = LTLVariable("a" if b else "b")
    f = ltl_interpret(formula, lookup)
    assert type(f) is bool
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = ltl_interpret(
        LTLNot(LTLVariable(b)), lambda _: pytest.fail("Unexpected lookup call")
    )
    assert type(f) is bool
    assert f is not b


@given(st.booleans(), st.booleans())
def test_and(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLAnd(LTLVariable(b0), LTLVariable(b1)),
        lambda _: pytest.fail("Unexpected lookup call"),
    )
    assert type(f) is bool
    assert f is (b0 and b1)


@given(st.booleans(), st.booleans())
def test_or(b0: bool, b1: bool) -> None:
    f = ltl_interpret(
        LTLOr(LTLVariable(b0), LTLVariable(b1)),
        lambda _: pytest.fail("Unexpected lookup call"),
    )
    assert type(f) is bool
    assert f is (b0 or b1)


@given(st.booleans())
def test_next(b: bool) -> None:
    f = ltl_interpret(
        LTLNext(LTLVariable(b)), lambda _: pytest.fail("Unexpected lookup call")
    )
    assert type(f) is bool
    assert f is b


@given(st.lists(st.booleans()))
def test_eventually(lst: List[bool]) -> None:
    expected = any(lst)

    f: Union[LTLFormula, bool] = LTLEventually(LTLVariable("a"))
    for b in lst:
        if type(f) is bool:
            break

        def lookup(name: str) -> bool:
            # name does not matter as there is only one variable
            return b

        f = ltl_interpret(cast(LTLFormula, f), lookup)

    if type(f) is LTLEventually:
        f = False

    assert f is expected

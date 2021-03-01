import pytest
from hypothesis import given, strategies as st
from ltlpy import LTLVariable, LTLNot, LTLAnd, LTLOr, LTLNext, ltl_interpret


@given(st.booleans())
def test_var(b: bool) -> None:
    f = ltl_interpret(LTLVariable(b), lambda _: pytest.fail("Unexpected lookup call"))
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

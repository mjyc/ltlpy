from hypothesis import given, strategies as st
from ltlpy import LTLVariable, LTLNot, LTLOr, interpret


@given(st.booleans())
def test_var(b: bool) -> None:
    f = interpret(LTLVariable(b))
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = interpret(LTLNot(LTLVariable(b)))
    assert type(f) is bool
    assert f is not b


@given(st.booleans(), st.booleans())
def test_or(b0: bool, b1: bool) -> None:
    f = interpret(LTLOr(LTLVariable(b0), LTLVariable(b1)))
    assert type(f) is bool
    assert f is (b0 or b1)

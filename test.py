from hypothesis import given, strategies as st
from ltlpy import LTLVariable, LTLNot, interpret


@given(st.booleans())
def test_var(b: bool) -> None:
    f = interpret(LTLVariable(b))
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = interpret(LTLNot(LTLVariable(b)))
    assert type(f) is bool
    assert f is not b

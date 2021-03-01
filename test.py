from hypothesis import given, strategies as st
from ltlpy import LTLVariable, interpret


@given(st.booleans())
def test_var(b: bool) -> None:
    f = LTLVariable(b)
    assert interpret(f) is b

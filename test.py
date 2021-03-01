from hypothesis import given, strategies as st
from ltlpy import LTLOperators, LTLFormula, interpret


@given(st.lists(st.booleans()))
def test_var(b: bool) -> None:
    f = LTLFormula(op=LTLOperators.VARIABLE, value=b)
    assert interpret(f) is b

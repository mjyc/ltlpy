from typing import List
from hypothesis import given, strategies as st
from ltlpy import LTLFormula, LTLVariable, LTLNot, LTLAnd, LTLOr, LTLNext, interpret


@given(st.booleans())
def test_var(b: bool) -> None:
    f = interpret(LTLVariable(b))
    assert type(f) is bool
    assert f is b


@given(st.booleans())
def test_not(b: bool) -> None:
    f = interpret(LTLNot(LTLVariable(b)))
    assert type(f) is bool
    assert f is not b


@given(st.booleans(), st.booleans())
def test_and(b0: bool, b1: bool) -> None:
    f = interpret(LTLAnd(LTLVariable(b0), LTLVariable(b1)))
    assert type(f) is bool
    assert f is (b0 and b1)


@given(st.booleans(), st.booleans())
def test_or(b0: bool, b1: bool) -> None:
    f = interpret(LTLOr(LTLVariable(b0), LTLVariable(b1)))
    assert type(f) is bool
    assert f is (b0 or b1)


@given(st.booleans())
def test_next(b: bool) -> None:
    f = interpret(LTLNext(LTLVariable(b)))
    assert type(f) is bool
    assert f is b


# @given(st.lists(st.booleans()))
# def test_eventually(lst: List[bool]) -> None:
#     expected = any(lst)
#     f = LTLEventually(LTLVariable(True))
#     for _ in lst:
#         if type(f) is not LTLFormula:
#             break
#         f = interpret(f)
#     1

#     while type(f) is LTLFormula
#     f = interpret(LTLEventually(LTLVariable(True)))
#     assert type(f) is bool
#     assert f is b

from hypothesis import given, note, strategies as st
from ltlpy import hello


@given(st.lists(st.integers()), st.randoms())
def test_shuffle_is_noop(ls, r):
    ls2 = list(ls)
    r.shuffle(ls2)
    note("Shuffle: %r" % (ls2))
    assert ls == ls2


# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    print("---hello", hello)
    assert func(3) == 5

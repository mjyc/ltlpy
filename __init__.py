from typing import cast, Union, Callable

LTLFormula = Union[
    "LTLVariable", "LTLNot", "LTLAnd", "LTLOr", "LTLNext", "LTLEventually"
]


class LTLVariable:
    def __init__(self, value: Union[bool, str]) -> None:
        self.value = value


class LTLNot:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


class LTLAnd:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right


class LTLOr:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right


class LTLNext:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


class LTLEventually:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


def ltl_interpret(
    formula: LTLFormula, lookup: Callable[[str], bool]
) -> Union[LTLFormula, bool, str]:
    if type(formula) is LTLVariable:
        value = cast(LTLVariable, formula).value
        if type(value) is bool:
            return value
        return lookup(cast(str, value))
    if type(formula) is LTLNot:
        f = ltl_interpret(cast(LTLNot, formula).value, lookup)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLAnd:
        f0 = ltl_interpret(cast(LTLAnd, formula).left, lookup)
        f1 = ltl_interpret(cast(LTLAnd, formula).right, lookup)
        if f0 is False:
            return False
        if f1 is False:
            return False
        if f0 is True and f1 is True:
            return True
        return LTLAnd(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLOr:
        f0 = ltl_interpret(cast(LTLOr, formula).left, lookup)
        f1 = ltl_interpret(cast(LTLOr, formula).right, lookup)
        if f0 is True:
            return True
        if f1 is True:
            return True
        if f0 is False and f1 is False:
            return False
        return LTLOr(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLNext:
        f = ltl_interpret(cast(LTLNot, formula).value, lookup)
        return f
    if type(formula) is LTLEventually:
        f = ltl_interpret(cast(LTLNot, formula).value, lookup)
        if f is True:
            return True
        if f is False:
            return formula
        return LTLOr(cast(LTLFormula, f), formula)

    raise Exception("Invalid formula")

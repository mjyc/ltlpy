from typing import cast, Union

LTLFormula = Union["LTLVariable", "LTLNot", "LTLAnd", "LTLOr", "LTLNext"]


class LTLVariable:
    def __init__(self, value: bool) -> None:
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


def interpret(formula: LTLFormula) -> Union[LTLFormula, bool]:
    if type(formula) is LTLVariable:
        return cast(LTLVariable, formula).value
    if type(formula) is LTLNot:
        f = interpret(cast(LTLNot, formula).value)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLAnd:
        f0 = interpret(cast(LTLAnd, formula).left)
        f1 = interpret(cast(LTLAnd, formula).right)
        if f0 is False:
            return False
        if f1 is False:
            return False
        if f0 is True and f1 is True:
            return True
        return LTLAnd(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLOr:
        f0 = interpret(cast(LTLOr, formula).left)
        f1 = interpret(cast(LTLOr, formula).right)
        if f0 is True:
            return True
        if f1 is True:
            return True
        if f0 is False and f1 is False:
            return False
        return LTLOr(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLNext:
        f = interpret(cast(LTLNot, formula).value)
        return f

    raise Exception("Invalid formula")

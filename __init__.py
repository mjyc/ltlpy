from typing import cast, Union

LTLFormula = Union["LTLVariable", "LTLNot", "LTLOr"]


class LTLVariable:
    def __init__(self, value: bool) -> None:
        self.value = value


class LTLNot:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


class LTLOr:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right


def interpret(formula: LTLFormula) -> Union[LTLFormula, bool]:
    if type(formula) is LTLVariable:
        return cast(LTLVariable, formula).value
    if type(formula) is LTLNot:
        f = interpret(cast(LTLNot, formula).value)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
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

    raise Exception("Invalid formula")

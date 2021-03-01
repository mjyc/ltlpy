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
        return formula.value
    if type(formula) is LTLNot:
        f = interpret(cast(LTLNot, formula).value)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLOr:
        f = interpret(cast(LTLOr, formula).left)
        f = interpret(cast(LTLOr, formula).right)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))

    raise Exception("Invalid formula")

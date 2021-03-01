from typing import cast, Union

LTLFormula = Union["LTLVariable", "LTLNot"]


class LTLVariable:
    def __init__(self, value: bool) -> None:
        self.value = value


class LTLNot:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


def interpret(formula: LTLFormula) -> Union[LTLFormula, bool]:
    if type(formula) is LTLVariable:
        return formula.value
    if type(formula) is LTLNot:
        f = interpret(cast(LTLNot, formula).value)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))

    raise Exception("Invalid formula")

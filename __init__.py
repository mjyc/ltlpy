from typing import Optional, Union

LTLFormula = Union["LTLVariable"]


class LTLVariable:
    def __init__(self, value: bool) -> None:
        self.value = value


def interpret(formula: LTLFormula) -> Optional[bool]:
    if type(formula) is LTLVariable:
        return formula.value
    return None

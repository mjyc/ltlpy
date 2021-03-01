from typing import cast, Union

from enum import Enum


class LTLOperators(Enum):
    VARIABLE = 'variable'
    NOT = 'not'
    AND = 'and'
    OR = 'or'
    NEXT = 'next'
    ALWAYS = 'always'
    EVENTUALLY = 'eventually'


class LTLFormula:
    def __init__(self, op: LTLOperators, value: Union["LTLFormula", bool]) -> None:
        self.op = op
        self.value = value


def interpret(formula: LTLFormula) -> Union[LTLFormula, bool]:
    # if formula is None:
    #     return None
    # elif type(formula) is bool:
    #     return formula

    if formula.op is LTLOperators.VARIABLE:  # type: ignore[union-attr]
        return formula.value
    elif formula.op is LTLOperators.NOT:
        f = interpret(formula.value)
        if f is None:
            return None
        elif type(f) is bool:
            return not f
        else:
            return LTLFormula(op=LTLOperators.NOT, value=f)

    raise Exception("Invalid formula")

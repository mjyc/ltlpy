from typing import Optional, Union
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
    def __init__(
        self, op: LTLOperators, value: Optional[Union["LTLFormula", bool]]
    ) -> None:
        self.op = op
        self.value = value


def interpret(formula: LTLFormula) -> Union[LTLFormula, bool, None]:
    if formula.op is LTLOperators.VARIABLE:
        return formula.value

    return None

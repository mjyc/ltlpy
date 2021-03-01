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
        self.next = value

from typing import Callable, Dict, Union, cast

LTLFormula = Union[
    "LTLVariable",
    "LTLNot",
    "LTLAnd",
    "LTLOr",
    "LTLNext",
    "LTLEventually",
    "LTLAlways",
]


class LTLVariable:
    def __init__(self, value: Union[bool, str]) -> None:
        self.value = value

    def __str__(self) -> str:
        if type(self.value) is bool:
            return "true" if self.value else "false"
        else:
            return cast(str, self.value)


class LTLNot:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"(not {str(self.value)})"


class LTLAnd:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({str(self.left)} and {str(self.right)})"


class LTLOr:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({str(self.left)} or {str(self.right)})"


class LTLNext:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"(next {str(self.value)})"


class LTLEventually:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"(eventually {str(self.value)})"


class LTLAlways:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"(always {str(self.value)})"


def ltl_interpret(
    formula: LTLFormula,
    get_lookup_table: Callable[[], Dict[str, Union[bool, Callable[[], bool]]]],
) -> Union[LTLFormula, bool]:
    print("---formula", formula)
    if type(formula) is LTLVariable:
        value = cast(LTLVariable, formula).value
        if type(value) is bool:
            return cast(bool, value)

        variable_name = cast(str, value)
        lookup_table = get_lookup_table()
        if variable_name in lookup_table:
            variable_value = lookup_table[variable_name]
            if type(variable_value) is bool:
                return cast(bool, variable_value)
            else:
                return cast(Callable[[], bool], variable_value)()

        return formula
    if type(formula) is LTLNot:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLAnd:
        f0 = ltl_interpret(cast(LTLAnd, formula).left, get_lookup_table)
        f1 = ltl_interpret(cast(LTLAnd, formula).right, get_lookup_table)
        if f0 is False or f1 is False:
            return False
        if f0 is True and f1 is True:
            return True
        if f0 is True:
            return cast(LTLFormula, f1)
        if f1 is True:
            return cast(LTLFormula, f0)
        return LTLAnd(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLOr:
        f0 = ltl_interpret(cast(LTLOr, formula).left, get_lookup_table)
        f1 = ltl_interpret(cast(LTLOr, formula).right, get_lookup_table)
        print("f0, f1", f0, f1)
        if f0 is True or f1 is True:
            return True
        if f0 is False and f1 is False:
            return False
        if f0 is False:
            return cast(LTLFormula, f1)
        if f1 is False:
            return cast(LTLFormula, f0)
        return LTLOr(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLNext:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        return f
    if type(formula) is LTLEventually:
        print("----cast(LTLEventually, formula)", cast(LTLEventually, formula))
        f = ltl_interpret(cast(LTLEventually, formula).value, get_lookup_table)
        print("----f", f)
        if f is True:
            return True
        if f is False:
            return formula
        return LTLOr(cast(LTLFormula, f), formula)
    if type(formula) is LTLAlways:
        f = ltl_interpret(cast(LTLAlways, formula).value, get_lookup_table)
        if f is False:
            return False
        if f is True:
            return formula
        return LTLAnd(cast(LTLFormula, f), formula)

    raise Exception("Invalid formula", formula)

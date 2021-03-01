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


class LTLAlways:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value


def ltl_interpret(
    formula: LTLFormula,
    get_lookup_table: Callable[[], Dict[str, Union[bool, Callable[[], None]]]],
) -> Union[LTLFormula, bool]:
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
                cast(Callable[[], None], variable_value)()
                return True

        return formula
    if type(formula) is LTLNot:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLAnd:
        f0 = ltl_interpret(cast(LTLAnd, formula).left, get_lookup_table)
        f1 = ltl_interpret(cast(LTLAnd, formula).right, get_lookup_table)
        if f0 is False:
            return False
        if f1 is False:
            return False
        if f0 is True and f1 is True:
            return True
        return LTLAnd(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLOr:
        f0 = ltl_interpret(cast(LTLOr, formula).left, get_lookup_table)
        f1 = ltl_interpret(cast(LTLOr, formula).right, get_lookup_table)
        if f0 is True:
            return True
        if f1 is True:
            return True
        if f0 is False and f1 is False:
            return False
        return LTLOr(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLNext:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        return f
    if type(formula) is LTLEventually:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        if f is True:
            return True
        if f is False:
            return formula
        return LTLOr(cast(LTLFormula, f), formula)
    if type(formula) is LTLAlways:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        if f is False:
            return False
        if f is True:
            return formula
        return LTLOr(cast(LTLFormula, f), formula)

    raise Exception("Invalid formula")

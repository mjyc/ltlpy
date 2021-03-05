from typing import Callable, Dict, List, Optional, Union, cast

LTLFormula = Union[
    "LTLVariable",
    "LTLNot",
    "LTLAnd",
    "LTLOr",
    "LTLNext",
    "LTLEventually",
    "LTLAlways",
    "LTLUntil",
]


class LTLVariable:
    def __init__(self, value: Union[bool, str]) -> None:
        self.value = value

    def __str__(self) -> str:
        if type(self.value) is bool:
            return f"LTLVariable({self.value})"
        else:
            return f'LTLVariable("{self.value}")'

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLVariable:
            return self.value == cast(LTLVariable, other).value
        return False


class LTLNot:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"LTLNot({str(self.value)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLNot:
            return self.value == cast(LTLNot, other).value
        return False


class LTLAnd:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"LTLAnd({str(self.left)}, {str(self.right)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLAnd:
            return (
                self.left == cast(LTLAnd, other).left
                and self.right == cast(LTLAnd, other).right
            )
        return False


class LTLOr:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"LTLOr({str(self.left)}, {str(self.right)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLOr:
            return (
                self.left == cast(LTLOr, other).left
                and self.right == cast(LTLOr, other).right
            )
        return False


class LTLNext:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"LTLNext({str(self.value)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLNext:
            return self.value == cast(LTLNext, other).value
        return False


class LTLEventually:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"LTLEventually({str(self.value)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLEventually:
            return self.value == cast(LTLEventually, other).value
        return False


class LTLAlways:
    def __init__(self, value: LTLFormula) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"LTLAlways({str(self.value)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLAlways:
            return self.value == cast(LTLAlways, other).value
        return False


class LTLUntil:
    def __init__(self, left: LTLFormula, right: LTLFormula) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"LTLUntil({str(self.left), str(self.right)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is LTLUntil:
            return (
                self.left == cast(LTLUntil, other).left
                and self.right == cast(LTLUntil, other).right
            )
        return False


def ltl_interpret(
    formula: LTLFormula,
    get_lookup_table: Callable[[], Dict[str, Union[bool, Callable[[], bool]]]],
    is_final: Optional[bool] = False,
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
                return cast(Callable[[], bool], variable_value)()

        return formula
    if type(formula) is LTLNot:
        f = ltl_interpret(cast(LTLNot, formula).value, get_lookup_table)
        if type(f) is bool:
            return not f
        return LTLNot(cast(LTLFormula, f))
    if type(formula) is LTLAnd:
        f0 = ltl_interpret(cast(LTLAnd, formula).left, get_lookup_table)
        if f0 is False:  # skip evaluating right
            return False
        f1 = ltl_interpret(cast(LTLAnd, formula).right, get_lookup_table)
        if f1 is False:
            return False
        if f0 is True and f1 is True:
            return True
        if f0 is True:  # prune left
            return cast(LTLFormula, f1)
        if f1 is True:  # prune right
            return cast(LTLFormula, f0)
        # prune repetitive branches in certain nested LTLAnd cases
        if type(f0) is LTLOr and cast(LTLOr, f0).left == f1:
            return LTLAnd(cast(LTLAnd, f0).right, cast(LTLFormula, f1))
        if type(f0) is LTLAnd and cast(LTLAnd, f0).right == f1:
            return LTLAnd(cast(LTLAnd, f0).left, cast(LTLFormula, f1))
        if type(f1) is LTLAnd and cast(LTLAnd, f1).left == f0:
            return LTLAnd(cast(LTLFormula, f0), cast(LTLAnd, f1).right)
        if type(f1) is LTLAnd and cast(LTLAnd, f1).right == f0:
            return LTLAnd(cast(LTLFormula, f0), cast(LTLAnd, f1).left)
        return LTLAnd(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLOr:
        f0 = ltl_interpret(cast(LTLOr, formula).left, get_lookup_table)
        if f0 is True:  # skip evaluating right
            return True
        f1 = ltl_interpret(cast(LTLOr, formula).right, get_lookup_table)
        if f1 is True:
            return True
        if f0 is False and f1 is False:
            return False
        if f0 is False:  # prune left
            return cast(LTLFormula, f1)
        if f1 is False:  # prune left
            return cast(LTLFormula, f0)
        # prune repetitive branches in certain nested LTLOr cases
        if type(f0) is LTLOr and cast(LTLOr, f0).left == f1:
            return LTLOr(cast(LTLOr, f0).right, cast(LTLFormula, f1))
        if type(f0) is LTLOr and cast(LTLOr, f0).right == f1:
            return LTLOr(cast(LTLOr, f0).left, cast(LTLFormula, f1))
        if type(f1) is LTLOr and cast(LTLOr, f1).left == f0:
            return LTLOr(cast(LTLFormula, f0), cast(LTLOr, f1).right)
        if type(f1) is LTLOr and cast(LTLOr, f1).right == f0:
            return LTLOr(cast(LTLFormula, f0), cast(LTLOr, f1).left)
        return LTLOr(cast(LTLFormula, f0), cast(LTLFormula, f1))
    if type(formula) is LTLNext:
        return cast(LTLNext, formula).value
    if type(formula) is LTLEventually:
        f = ltl_interpret(cast(LTLEventually, formula).value, get_lookup_table)
        if f is True:
            return True
        if f is False:
            return formula if not is_final else False
        # remove nested eventually
        if f is cast(LTLEventually, formula).value:
            return formula
        return LTLOr(cast(LTLFormula, f), formula)
    if type(formula) is LTLAlways:
        f = ltl_interpret(cast(LTLAlways, formula).value, get_lookup_table)
        if f is False:
            return False
        if f is True:
            return formula if not is_final else True
        # remove nested always
        if f is cast(LTLAlways, formula).value:
            return formula
        return LTLAnd(cast(LTLFormula, f), formula)

    # TODO: finish it
    if type(formula) is LTLUntil:
        f0 = ltl_interpret(cast(LTLUntil, formula).left, get_lookup_table)
        if f is False:
            return False
        if f is True:
            return formula if not is_final else True
        # remove nested always
        if f is cast(LTLAlways, formula).value:
            return formula
        return LTLAnd(cast(LTLFormula, f), formula)

    raise Exception("Invalid formula", formula)


def get_variable_names(
    formula: LTLFormula, names: Optional[List[str]] = None
) -> List[str]:
    if names is None:
        names = []

    if type(formula) is LTLVariable:
        value = cast(LTLVariable, formula).value
        if type(value) is bool:
            return names
        variable_name = cast(str, value)
        names.append(variable_name)
        return names
    if type(formula) is LTLNot:
        get_variable_names(cast(LTLNot, formula).value, names)
        return names
    if type(formula) is LTLAnd:
        get_variable_names(cast(LTLAnd, formula).left, names)
        get_variable_names(cast(LTLAnd, formula).right, names)
        return names
    if type(formula) is LTLOr:
        get_variable_names(cast(LTLOr, formula).left, names)
        get_variable_names(cast(LTLOr, formula).right, names)
        return names
    if type(formula) is LTLNext:
        get_variable_names(cast(LTLNext, formula).value, names)
        return names
    if type(formula) is LTLEventually:
        get_variable_names(cast(LTLEventually, formula).value, names)
        return names
    if type(formula) is LTLAlways:
        get_variable_names(cast(LTLAlways, formula).value, names)
        return names

    raise Exception("Invalid formula", formula)

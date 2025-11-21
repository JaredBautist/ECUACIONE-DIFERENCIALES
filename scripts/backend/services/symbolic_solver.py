from typing import Dict, List, Optional, Tuple

from sympy import Eq, Function, latex, symbols
from sympy import dsolve  # type: ignore

from .parser import parse_equation

x = symbols("x")
DEFAULT_FUNC = Function("y")


def solve_symbolic(eq_expr: str, ics: Optional[Dict] = None, func: Function = DEFAULT_FUNC):
    """Resuelve simbólicamente una ecuación diferencial (1ra o 2da orden) con CI opcionales."""
    left, right = parse_equation(eq_expr)
    eq = Eq(left, right) if right is not None else left
    solution = dsolve(eq, func(x), ics=ics) if ics else dsolve(eq, func(x))
    solutions = solution if isinstance(solution, (list, tuple)) else [solution]
    return solutions


def solve_symbolic_system(
    eqs: List[str],
    variables: Optional[List[str]] = None,
    ics: Optional[Dict] = None,
) -> List:
    """Resuelve simbólicamente sistemas (si SymPy puede resolverlos)."""
    funcs = [Function(v) for v in variables] if variables else []
    parsed_eqs: List[Eq] = []
    for idx, expr in enumerate(eqs):
        func = funcs[idx] if idx < len(funcs) else Function(f"y{idx+1}")
        left, right = parse_equation(expr)
        parsed_eqs.append(Eq(left, right) if right is not None else left)
    solution = dsolve(parsed_eqs, ics=ics) if ics else dsolve(parsed_eqs)
    return solution if isinstance(solution, (list, tuple)) else [solution]


def to_latex_list(solutions) -> List[str]:
    sols = solutions if isinstance(solutions, (list, tuple)) else [solutions]
    return [latex(sol) for sol in sols]


def solution_summary(solutions) -> str:
    sols = solutions if isinstance(solutions, (list, tuple)) else [solutions]
    return "; ".join([latex(sol) for sol in sols])

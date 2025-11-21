from typing import Callable, List, Sequence, Tuple

import numpy as np
from sympy import Derivative, Eq, Function, symbols, solve
from sympy.utilities.lambdify import lambdify

x = symbols("x")


def build_rhs_scalar(eq: Eq, func: Function) -> Callable[[float, float], float]:
    """Obtiene f(x, y) de una ecuación Derivative(y,x) = rhs."""
    if not isinstance(eq, Eq):
        raise ValueError("La ecuación debe ser una igualdad para método numérico.")

    lhs = eq.lhs
    rhs = eq.rhs
    target = Derivative(func(x), x)
    if lhs != target:
        # intentar despejar
        rhs_candidate = solve(eq, target)
        if rhs_candidate:
            rhs = rhs_candidate[0]
    f = lambdify((x, func(x)), rhs, modules="numpy")
    return lambda xv, yv: float(f(xv, yv))


def euler(f: Callable[[float, float], float], x0: float, y0: float, h: float, n: int):
    xs = [x0]
    ys = [y0]
    for _ in range(n):
        y0 = y0 + h * f(x0, y0)
        x0 = x0 + h
        xs.append(x0)
        ys.append(y0)
    return xs, ys


def rk4(f: Callable[[float, float], float], x0: float, y0: float, h: float, n: int):
    xs = [x0]
    ys = [y0]
    for _ in range(n):
        k1 = f(x0, y0)
        k2 = f(x0 + h / 2, y0 + h * k1 / 2)
        k3 = f(x0 + h / 2, y0 + h * k2 / 2)
        k4 = f(x0 + h, y0 + h * k3)
        y0 = y0 + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x0 = x0 + h
        xs.append(x0)
        ys.append(y0)
    return xs, ys


# --- Sistemas ---


def build_rhs_system(eqs: Sequence[Eq], funcs: Sequence[Function]):
    rhs_funcs = []
    for eq, func in zip(eqs, funcs):
        target = Derivative(func(x), x)
        rhs = eq.rhs
        if eq.lhs != target:
            rhs_candidate = solve(eq, target)
            if rhs_candidate:
                rhs = rhs_candidate[0]
        rhs_funcs.append(rhs)
    lambda_rhs = lambdify(
        (x, *[f(x) for f in funcs]), rhs_funcs, modules="numpy"
    )
    def f_system(xv, y_vec):
        args = [xv, *list(y_vec)]
        vals = lambda_rhs(*args)
        return np.array(vals, dtype=float)
    return f_system


def euler_system(f_system, x0: float, y0: List[float], h: float, n: int):
    xs = [x0]
    ys = [np.array(y0, dtype=float)]
    for _ in range(n):
        y_new = ys[-1] + h * f_system(x0, ys[-1])
        x0 = x0 + h
        xs.append(x0)
        ys.append(y_new)
    return xs, ys


def rk4_system(f_system, x0: float, y0: List[float], h: float, n: int):
    xs = [x0]
    ys = [np.array(y0, dtype=float)]
    for _ in range(n):
        y_curr = ys[-1]
        k1 = f_system(x0, y_curr)
        k2 = f_system(x0 + h / 2, y_curr + h * k1 / 2)
        k3 = f_system(x0 + h / 2, y_curr + h * k2 / 2)
        k4 = f_system(x0 + h, y_curr + h * k3)
        y_new = y_curr + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x0 = x0 + h
        xs.append(x0)
        ys.append(y_new)
    return xs, ys

from fastapi import APIRouter, HTTPException
from sympy import Eq, Function, latex, symbols

from ..services import (
    parser,
    symbolic_solver,
    numeric_solver,
    steps as stepgen,
    qwen_client,
)
from ..services.advanced_solver import advanced_solver
import re
from ..models.schemas import (
    SolveRequest,
    SolveResponse,
    SystemSolveRequest,
    ValidateRequest,
)

router = APIRouter()
x = symbols("x")


def ci_dict_to_adv_ics(ci_dict: dict) -> dict:
    """Convierte las CI parseadas a formato {'x0':..., 'y0':..., 'yp0':..., 'ypp0':...}."""
    if not ci_dict:
        return {}
    adv = {}
    for key, val in ci_dict.items():
        try:
            # key puede ser y(x0) o Derivative(y(x), x).subs(x, x0)
            if hasattr(key, "func") and key.func.__name__ == "y":
                x0_val = key.args[0]
                adv.setdefault("x0", x0_val)
                adv["y0"] = val
            elif key.is_Number:
                continue
            elif key.is_Derivative:
                order = key.derivative_count
                x0_val = key.args[0].args[0]
                adv.setdefault("x0", x0_val)
                if order == 1:
                    adv["yp0"] = val
                elif order == 2:
                    adv["ypp0"] = val
            elif hasattr(key, "subs"):
                # Derivada con .subs(x, x0)
                if key.has(Derivative):
                    order = list(key.atoms(Derivative))[0].derivative_count
                    x0_candidates = key.atoms(Symbol)
                    if x not in x0_candidates:
                        for sym in x0_candidates:
                            adv.setdefault("x0", sym)
                    if order == 1:
                        adv["yp0"] = val
                    elif order == 2:
                        adv["ypp0"] = val
        except Exception:
            continue
    return adv


@router.post("/solve", response_model=SolveResponse)
async def solve_equation(req: SolveRequest):
    try:
        eq_str, ci_segments = parser.normalize_equation(req.equation)
        ci_dict = parser.parse_initial_conditions(ci_segments) if ci_segments else {}
        left, right = parser.parse_equation(eq_str)
        eq_obj = Eq(left, right) if right is not None else left

        # Mapeo de CI del request al formato del solver avanzado (y0, y1, y2)
        adv_ics = None
        if req.initial_conditions:
            adv_ics = {
                "x0": req.initial_conditions.x0,
                "y0": req.initial_conditions.y0,
                "yp0": req.initial_conditions.y1,
                "ypp0": req.initial_conditions.y2,
            }

        # Numérico
        if req.method.startswith("numeric"):
            if not req.initial_conditions:
                raise HTTPException(status_code=400, detail="Método numérico requiere condiciones iniciales.")
            if not isinstance(eq_obj, Eq):
                raise HTTPException(status_code=400, detail="La ecuación debe estar en forma explícita para método numérico.")
            func = Function("y")
            f = numeric_solver.build_rhs_scalar(eq_obj, func)
            h = req.step or 0.1
            n = req.steps or 50
            solver = numeric_solver.euler if req.method.endswith("euler") else numeric_solver.rk4
            xs, ys = solver(f, req.initial_conditions.x0, req.initial_conditions.y0, h, n)
            trace = [{"x": float(xi), "y": float(yi)} for xi, yi in zip(xs, ys)]
            return SolveResponse(
                originalEquation=req.equation,
                solution="Trayectoria numérica",
                steps=stepgen.numeric_steps(req.method, h, n),
                numeric_trace=trace,
            )

        # Simbólico con solver avanzado según tipo
        adv_map = {
            "general": advanced_solver.solve_general,
            "separable": advanced_solver.solve_separable,
            "homogeneous": advanced_solver.solve_homogeneous,
            "linear": advanced_solver.solve_linear,
            "bernoulli": advanced_solver.solve_bernoulli,
            "second_order_const": advanced_solver.solve_second_order_constant_coeff,
            "reducible": advanced_solver.solve_reducible_to_first_order,
        }

        # Mezclar CI de request + las extraídas del string
        merged_adv_ics = {}
        if req.initial_conditions:
            merged_adv_ics = {
                "x0": req.initial_conditions.x0,
                "y0": req.initial_conditions.y0,
                "yp0": req.initial_conditions.y1,
                "ypp0": req.initial_conditions.y2,
            }
        # Complementar con las CI parseadas del string
        merged_adv_ics = {k: v for k, v in merged_adv_ics.items() if v is not None}
        parsed_adv_ics = ci_dict_to_adv_ics(ci_dict)
        merged_adv_ics.update({k: v for k, v in parsed_adv_ics.items() if v is not None})

        if req.equation_type == "exact":
            # Intentar extraer M y N si viene en forma M dx + N dy = 0
            match = re.match(r"^(?P<M>.*?)dx\+(?P<N>.*?)dy=0$", eq_str)
            if match:
                result = advanced_solver.solve_exact(match.group("M"), match.group("N"))
            else:
                raise HTTPException(status_code=400, detail="Para exactas usa formato M(x,y)dx + N(x,y)dy = 0")
        elif req.equation_type == "integrating_factor":
            match = re.match(r"^(?P<M>.*?)dx\+(?P<N>.*?)dy=0$", eq_str)
            if match:
                result = advanced_solver.find_integrating_factor(match.group("M"), match.group("N"))
            else:
                raise HTTPException(status_code=400, detail="Para factor integrante usa formato M(x,y)dx + N(x,y)dy = 0")
        elif req.equation_type in adv_map:
            # Usar la ecuación ya normalizada para evitar problemas con '^' y notación
            result = adv_map[req.equation_type](eq_str, initial_conditions=merged_adv_ics or None)
        else:
            # Fallback al solver simbólico genérico
            solutions = symbolic_solver.solve_symbolic(eq_str, ci_dict if ci_dict else None)
            sols_latex = symbolic_solver.to_latex_list(solutions)
            qwen_feedback = None
            if req.with_qwen:
                qwen_feedback = await qwen_client.ask_qwen(
                    f"Valida o mejora la solución {sols_latex} para la ecuación: {req.equation}"
                )
            return SolveResponse(
                originalEquation=latex(eq_obj),
                solution=sols_latex,
                steps=stepgen.symbolic_steps(
                    req.equation_type,
                    sols_latex[0] if sols_latex else "",
                    latex(eq_obj),
                ),
                qwen_feedback=qwen_feedback,
            )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "No se pudo resolver"))

        sol_latex = result.get("solution_latex") or result.get("solution")
        qwen_feedback = None
        if req.with_qwen:
            qwen_feedback = await qwen_client.ask_qwen(
                f"Valida o mejora la solución {sol_latex} para la ecuación: {req.equation}"
            )
        return SolveResponse(
            originalEquation=req.equation,
            solution=[sol_latex],
            steps=stepgen.symbolic_steps(
                req.equation_type or result.get("method", ""),
                sol_latex,
                latex(eq_obj),
            ),
            qwen_feedback=qwen_feedback,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/system", response_model=SolveResponse)
async def solve_system(req: SystemSolveRequest):
    try:
        funcs = [Function(v) for v in req.variables] if req.variables else []
        parsed_eqs = []
        ci_dict = {}
        for expr in req.equations:
            eq_str, ic_segments = parser.normalize_equation(expr)
            left, right = parser.parse_equation(eq_str)
            parsed_eqs.append(Eq(left, right) if right is not None else left)
            if ic_segments:
                ci_dict.update(parser.parse_initial_conditions(ic_segments))

        if req.method.startswith("numeric"):
            if not req.initial_conditions or not req.initial_conditions.system:
                raise HTTPException(
                    status_code=400,
                    detail="Método numérico para sistema requiere initial_conditions.system con valores iniciales.",
                )
            if any(not isinstance(eq, Eq) for eq in parsed_eqs):
                raise HTTPException(status_code=400, detail="Cada ecuación del sistema debe estar en forma de igualdad para método numérico.")
            funcs = funcs or [Function(f"y{i+1}") for i in range(len(parsed_eqs))]
            f_sys = numeric_solver.build_rhs_system(parsed_eqs, funcs)
            h = req.step or 0.1
            n = req.steps or 50
            solver = numeric_solver.euler_system if req.method.endswith("euler") else numeric_solver.rk4_system
            xs, ys = solver(f_sys, req.initial_conditions.x0, req.initial_conditions.system, h, n)
            trace = [
                {"x": float(xi), **{f"y{i+1}": float(val) for i, val in enumerate(vec)}}
                for xi, vec in zip(xs, ys)
            ]
            return SolveResponse(
                originalEquation="; ".join(req.equations),
                solution="Trayectoria numérica",
                steps=stepgen.numeric_steps(req.method, h, n),
                numeric_trace=trace,
            )

        # Simbólico sistema
        solutions = symbolic_solver.solve_symbolic_system(req.equations, req.variables, ci_dict if ci_dict else None)
        sols_latex = symbolic_solver.to_latex_list(solutions)
        return SolveResponse(
            originalEquation="; ".join(req.equations),
            solution=sols_latex,
            steps=stepgen.symbolic_steps("sistema", solutions),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate")
async def validate_solution(req: ValidateRequest):
    feedback = await qwen_client.ask_qwen(
        f"Valida la solución propuesta {req.proposed_solution} para la ecuación {req.equation}"
    )
    return {"feedback": feedback}

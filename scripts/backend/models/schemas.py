from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class InitialConditions(BaseModel):
    x0: float
    y0: float
    y1: Optional[float] = None
    y2: Optional[float] = None
    system: Optional[List[float]] = None  # Para sistemas: valores iniciales de cada variable


class SolveRequest(BaseModel):
    equation: str
    equation_type: Optional[str] = Field(
        default=None, description="Tipo de ecuación (separable, linear, exact, etc.)"
    )
    method: Literal["symbolic", "numeric:euler", "numeric:rk4"] = "symbolic"
    initial_conditions: Optional[InitialConditions] = None
    step: Optional[float] = Field(default=0.1, description="Tamaño de paso para métodos numéricos")
    steps: Optional[int] = Field(default=50, description="Número de iteraciones para métodos numéricos")
    with_qwen: bool = Field(default=False, description="Solicitar validación o explicación con Qwen")


class SystemSolveRequest(BaseModel):
    equations: List[str]
    variables: Optional[List[str]] = None
    method: Literal["numeric:euler", "numeric:rk4"] = "numeric:rk4"
    initial_conditions: InitialConditions
    step: Optional[float] = 0.1
    steps: Optional[int] = 50
    with_qwen: bool = False


class ValidateRequest(BaseModel):
    equation: str
    proposed_solution: str


class SolveResponse(BaseModel):
    originalEquation: str
    solution: Any
    steps: List[Dict[str, Any]]
    numeric_trace: Optional[List[Dict[str, float]]] = None
    qwen_feedback: Optional[str] = None

from operator import add, mul, sub, truediv
from typing import Callable, Optional
from urllib.parse import quote

from fastapi import APIRouter
from pydantic import BaseModel

from app.infra.chain import ChainWithDefaultHandler as Chain

router = APIRouter(prefix="/simple")


class SimpleInfo(BaseModel):
    pass


def handle_operator(
    sign: str, op: Callable[[int | float, int | float], int | float]
) -> Callable[[str], Optional[int | float]]:
    def calc(expr: str) -> Optional[int | float]:
        l_term, *terms = expr.split(sign)
        if terms:
            acc = get_calc(l_term)
            for term in terms:
                acc = op(acc, get_calc(term))
            return acc
        return None

    return calc


def handle_value(expr: str, /) -> int | float:
    return int(expr) if (value := float(expr)).is_integer() else value


calc_chain = (
    Chain(default_handler=handle_value)
    | handle_operator("+", add)
    | handle_operator("-", sub)
    | handle_operator("*", mul)
    | handle_operator("/", truediv)
)


class ExprDTO(BaseModel):
    expr: str
    url_arg: str


def make_expr_dto(expr: str) -> ExprDTO:
    return ExprDTO(expr=expr, url_arg=quote(expr))


@router.get("/")
def get_entry() -> SimpleInfo:
    return SimpleInfo()


@router.get("/calc")
def get_calc(expr: str) -> int | float:
    return calc_chain(expr)


@router.get("/add")
def get_sum(l_expr: str, r_expr: str) -> ExprDTO:
    return make_expr_dto(f"{l_expr}+{r_expr}")


@router.get("/sub")
def get_diff(l_expr: str, r_expr: str) -> ExprDTO:
    return make_expr_dto(f"{l_expr}-{r_expr}")


@router.get("/mul")
def get_prod(l_expr: str, r_expr: str) -> ExprDTO:
    return make_expr_dto(f"{l_expr}*{r_expr}")


@router.get("/div")
def get_quot(l_expr: str, r_expr: str) -> ExprDTO:
    return make_expr_dto(f"{l_expr}/{r_expr}")

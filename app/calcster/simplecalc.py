from urllib.parse import quote

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/simple")


class ExprDTO(BaseModel):
    expr: str
    url_arg: str


def make_expr_dto(expr: str) -> ExprDTO:
    return ExprDTO(expr=expr, url_arg=quote(expr))


@router.get("/")
def get_calc(expr: str) -> int | float:
    return eval(expr)


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

from numbers import Number
from typing import Callable

from fastapi import APIRouter, Request

router = APIRouter(prefix="/calc")


@router.get("/simple")
def get_simple_calc(expr: str) -> int | float:
    return eval(expr)


@router.get("/one-operation")
def get_one_operation_calc(expr: str) -> int | float:
    return eval(expr)


@router.get("/")
def get_calc_list(request: Request) -> list[str]:
    def url_for(endpoint: Callable) -> str:
        return str(request.url_for(endpoint.__name__))

    return [url_for(get_simple_calc), url_for(get_one_operation_calc)]

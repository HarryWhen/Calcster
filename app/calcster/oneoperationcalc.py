from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/one-operation")


class OneOperationInfo(BaseModel):
    pass


@router.get("/", name=__name__)
def get_entry() -> OneOperationInfo:
    return OneOperationInfo()


@router.get("/calc")
def get_calc(l_value: int | float, r_value: int | float, op: str) -> int | float:
    match op:
        case "+":
            return get_sum(l_value, r_value)
        case "-":
            return get_diff(l_value, r_value)
        case "*":
            return get_prod(l_value, r_value)
        case "/":
            return get_quot(l_value, r_value)
    raise ValueError(f"Unknown op: {op}")


@router.get("/add")
def get_sum(l_value: int | float, r_value: int | float) -> int | float:
    return l_value + r_value


@router.get("/sub")
def get_diff(l_value: int | float, r_value: int | float) -> int | float:
    return l_value - r_value


@router.get("/mul")
def get_prod(l_value: int | float, r_value: int | float) -> int | float:
    return l_value * r_value


@router.get("/div")
def get_quot(l_value: int | float, r_value: int | float) -> int | float:
    return l_value / r_value

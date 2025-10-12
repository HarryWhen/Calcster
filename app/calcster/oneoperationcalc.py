from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/one-operation")


class OneOperationInfo(BaseModel):
    pass


@router.get("/")
def get_entry() -> OneOperationInfo:
    return OneOperationInfo()


@router.get("/calc")
def get_calc(expr: str) -> int | float:
    return eval(expr)

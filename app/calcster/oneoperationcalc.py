from fastapi import APIRouter

router = APIRouter(prefix="/one-operation")


@router.get("/")
def get_calc(expr: str) -> int | float:
    return eval(expr)

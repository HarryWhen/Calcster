from fastapi import APIRouter

router = APIRouter(prefix="/simple")


@router.get("/")
def get_calc(expr: str) -> int | float:
    return eval(expr)

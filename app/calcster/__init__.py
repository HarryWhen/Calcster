from typing import Callable

from fastapi import APIRouter, Request

from . import oneoperationcalc, simplecalc

router = APIRouter(prefix="/calc")
router.include_router(oneoperationcalc.router)
router.include_router(simplecalc.router)


@router.get("/")
def get_calc_list(request: Request) -> list[str]:
    def url_for(endpoint: Callable) -> str:
        return str(request.url_for(endpoint.__name__))

    return [
        url_for(oneoperationcalc.get_calc),
        url_for(simplecalc.get_calc),
    ]

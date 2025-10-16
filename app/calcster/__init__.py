from types import ModuleType

from fastapi import APIRouter, Request

from app import app

from . import oneoperationcalc, simplecalc

router = APIRouter(prefix="/calcster")
router.include_router(oneoperationcalc.router)
router.include_router(simplecalc.router)


@router.get("/")
def get_calc_list() -> list[str]:
    def url_for(module_with_entry: ModuleType) -> str:
        return app.url_path_for(module_with_entry.__name__)

    return [
        url_for(oneoperationcalc),
        url_for(simplecalc),
    ]

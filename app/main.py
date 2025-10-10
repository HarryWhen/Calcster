from . import app
from .calcster import router

app.include_router(router)

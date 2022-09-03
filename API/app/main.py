from fastapi import FastAPI
from db import database, models
from routers import import_router, info_router

models.base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(import_router.router, prefix="/update",tags=["update"])
app.include_router(info_router.router, prefix="/info",tags=["info"])
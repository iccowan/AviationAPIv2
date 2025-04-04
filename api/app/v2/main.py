from fastapi import FastAPI
from .routers import charts

app = FastAPI()

app.include_router(charts.router)

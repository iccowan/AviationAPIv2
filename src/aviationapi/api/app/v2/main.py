from fastapi import FastAPI

from .routers import airports, charts

app = FastAPI()

app.include_router(charts.router)
app.include_router(airports.router)

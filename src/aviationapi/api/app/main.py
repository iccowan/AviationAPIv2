from fastapi import FastAPI
from mangum import Mangum

from .v2 import main as v2

app = FastAPI()
handler = Mangum(app)

app.mount("/v2", v2.app)

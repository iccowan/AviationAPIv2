from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get('/')
async def root():
    return {'Hello': 'World'}


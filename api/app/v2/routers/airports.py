from fastapi import APIRouter

router = APIRouter(
    prefix = '/airports'
)

@router.get('')
async def airports():
    return ['KATL', 'KCLT', 'KLUK']

@router.get('/exists')
async def airport_exists(airport: str):
    return airport == 'KATL'

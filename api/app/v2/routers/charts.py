from fastapi import APIRouter

router = APIRouter(
    prefix = '/charts'
)

@router.get('')
async def charts(airport: str, group: int = 1):
    return {'airport': airport, 'group': group}

@router.get('/changes')
async def chart_changes(airport: str, chart_name: str = None):
    return {'airport': airport, 'chart_name': chart_name}

@router.get('/afd')
async def afd(airport: str):
    return {'airport': airport}

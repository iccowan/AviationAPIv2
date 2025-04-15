from fastapi import APIRouter

router = APIRouter(
    prefix = '/charts'
)

@router.get('')
async def charts(airport: str, group: int = 1, airac: int = 0):
    return {'airport': airport, 'group': group, 'airac': airac}

@router.get('/changes')
async def chart_changes(airport: str, chart_name: str = None, airac: int = 0):
    return {'airport': airport, 'chart_name': chart_name, 'airac': airac}

@router.get('/afd')
async def afd(airport: str, airac: int = 0):
    return {'airport': airport, 'airac': airac}

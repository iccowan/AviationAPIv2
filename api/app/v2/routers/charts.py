from fastapi import APIRouter

router = APIRouter(
    prefix = '/charts'
)

@router.get('/')
async def main():
    return {'hello': 'world'}

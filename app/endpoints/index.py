from fastapi import APIRouter
from starlette.responses import RedirectResponse

index_router = APIRouter(tags=['Index'], include_in_schema=False)


@index_router.get('/')
async def homepage() -> RedirectResponse:
    return RedirectResponse('/docs')

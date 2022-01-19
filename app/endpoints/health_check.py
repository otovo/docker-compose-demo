import asyncio
import logging
import socket

from fastapi import APIRouter
from starlette.responses import Response

from app.core import state

logger = logging.getLogger(__name__)

health_router = APIRouter(prefix='/health', tags=['Health'])


@health_router.get('', status_code=204)
async def health() -> Response:
    logger.info('-> health check OK!')
    try:
        await asyncio.wait_for(state.database.execute('SELECT 1'), timeout=1)
    except (asyncio.TimeoutError, socket.gaierror):
        return Response(status_code=503)
    return Response(status_code=204)

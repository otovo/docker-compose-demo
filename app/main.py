import contextlib
import logging
from typing import TYPE_CHECKING

from aioredis import from_url
from databases import Database
from fastapi import FastAPI

from app.core import state
from app.core.config import settings
from app.core.logging import configure_logging
from app.endpoints import base_router

if TYPE_CHECKING:
    from typing import Any, AsyncGenerator

    from aioredis import Redis

logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(*args: 'Any', **kwargs: 'Any') -> 'AsyncGenerator[None, None]':
    """
    Spins up redis/postgres connections on startup, and close on shutdown.
    """
    redis_: 'Redis' = await from_url(settings.REDIS_URL)  # type: ignore[no-untyped-call]
    database_ = Database(url=settings.DATABASE_URL.replace(scheme='postgresql'))

    configure_logging()
    logger.info('Starting up')

    async with database_ as d_conn, redis_ as r_conn:
        state.database = d_conn
        state.redis = r_conn
        yield
        logger.info('Shutting down')


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    version='v1',
    lifespan=lifespan,  # doesn't do anything
)
app.include_router(base_router)

# Apparently FastAPI doesn't really support Starlette's
# lifespan, so we use this hack for the demo project
app.router.lifespan_context = lifespan

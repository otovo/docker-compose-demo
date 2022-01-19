from typing import TYPE_CHECKING

from databases import DatabaseURL
from pydantic import BaseSettings, validator

if TYPE_CHECKING:
    from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    DEBUG: bool = False

    REDIS_URL: str
    DATABASE_URL: DatabaseURL

    @validator('DATABASE_URL', pre=True)
    def set_database_url(cls, v: 'Optional[str]') -> DatabaseURL:
        if not v:
            raise ValueError('DATABASE_URL not found')
        if 'postgresql' not in v and 'postgres' in v:
            v = v.replace('postgres', 'postgresql')
        if 'asyncpg' not in v:
            v = v.replace('postgresql', 'postgresql+asyncpg')
        return DatabaseURL(v)


settings = Settings(_env_file='.env')  # type: ignore[call-arg]

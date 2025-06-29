from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Setting(BaseSettings):
    model_config = SettingsConfigDict()

    ALLOWED_ORIGINS: list[str] = Field(['*'])

    LOG_LEVEL: str = Field('INFO')

    DB_URL: str

    SEARCH_RATE_LIMIT: int = Field(1000)
    GENERAL_RATE_LIMIT: int = Field(100)
    RATE_LIMIT_WINDOW: int = Field(3600)

    MAX_PAGE_SIZE: int = Field(100)

    @property
    def db_url(self) -> URL:
        return make_url(self.DB_URL)

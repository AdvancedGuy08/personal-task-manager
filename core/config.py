from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = Field(default="")
    ECHO: bool = Field(default=True, validation_alias="DATABASE_ECHO")


config = Config()

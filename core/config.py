from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = Field(default="")
    ECHO: bool = Field(default=True, validation_alias="DATABASE_ECHO")

    class Config:
        env_file = ".env"


config = Config()

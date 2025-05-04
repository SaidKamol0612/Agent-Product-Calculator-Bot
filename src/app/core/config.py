from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class BotSettings(BaseModel):
    token: str


class DataBaseSettings(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BOT__",
    )

    bot: BotSettings
    db: DataBaseSettings


settings = Settings()

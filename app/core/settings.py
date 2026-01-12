from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MailSettings(BaseModel):
    smtp_port: int = 465
    smtp_secure: bool = True

    timeout: int = 10
    smtp_host: str = ""
    user: str = ""
    password: str = ""
    admin: str = ""


class FastAPISettings(BaseModel):
    title: str = "Notify Service"
    version: str = "1.0.0"
    docs: str | None = "/docs"
    redoc: str | None = "/redoc"
    openapi: str | None = "/openapi.json"


class CORSSettings(BaseModel):
    allowed_origins: list[str] = [""]


class BotSettings(BaseModel):
    target_chat_id: int = 0
    notify_url: str = ""
    ping_url: str = ""


class GunicornSettings(BaseModel):
    bind: str = ""
    workers: int = 1
    worker_class: str = "uvicorn.workers.UvicornWorker"

    timeout: int = 30
    keepalive: int = 5
    graceful_timeout: int = 30

    access_log_format: str = ""
    error_logfile: str = ""
    access_logfile: str = ""
    loglevel: str = "warning"


class Settings(BaseSettings):
    env: str = ""
    port: int = 0
    host: str = "0.0.0.0"
    pythonunbuffered: bool = True

    fastapi: FastAPISettings = FastAPISettings()
    cors: CORSSettings = CORSSettings()
    mail: MailSettings = MailSettings()
    bot: BotSettings = BotSettings()
    gunicorn: GunicornSettings = GunicornSettings()

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    s = Settings()
    return s


settings = Settings()

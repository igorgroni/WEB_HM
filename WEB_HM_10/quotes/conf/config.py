from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name: str
    db_user: str
    password: str
    host: str
    port: str
    email_backend: str
    email_host: str
    email_port: int
    email_starttls: bool
    email_use_ssl: bool
    email_use_tls: bool
    email_host_user: str
    email_host_password: str
    default_from_email: str

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

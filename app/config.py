import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    seed_data: bool
    log_level: str


def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "RU-ometro"),
        app_version=os.getenv("APP_VERSION", "dev"),
        seed_data=os.getenv("SEED_DATA", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info"),
    )

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


class YamlConfigSettingsSource(PydanticBaseSettingsSource):

    def get_field_value(self, field, field_name: str) -> tuple[Any, str, bool]:
        return None, "", False

    def __call__(self) -> dict[str, Any]:
        config_path = Path(__file__).resolve().parents[1] / "config.yaml"

        if not config_path.exists():
            return {}

        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}


class Settings(BaseSettings):
    app_name: str = "User Service API"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

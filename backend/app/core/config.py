from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class Settings:
    app_name: str = "project-list-plugin"
    env: str = "dev"
    db_url: str = "sqlite:///./dev.db"
    excel_upload_dir: str = "./uploads"
    excel_export_dir: str = "./exports"
    secret_key: str = "change-me-in-production"
    log_level: str = "DEBUG"
    import_batch_size: int = 500
    auth_token_ttl_minutes: int = 480
    default_admin_username: str = "admin"
    default_admin_password: str = "admin123456"

    @property
    def upload_path(self) -> Path:
        return Path(self.excel_upload_dir)

    @property
    def export_path(self) -> Path:
        return Path(self.excel_export_dir)


@lru_cache
def get_settings() -> Settings:
    env_path = Path(".env")
    dotenv = _load_dotenv(env_path)

    def read(name: str, default: str) -> str:
        return os.getenv(name, dotenv.get(name, default))

    return Settings(
        app_name=read("APP_NAME", Settings.app_name),
        env=read("ENV", Settings.env),
        db_url=read("DB_URL", Settings.db_url),
        excel_upload_dir=read("EXCEL_UPLOAD_DIR", Settings.excel_upload_dir),
        excel_export_dir=read("EXCEL_EXPORT_DIR", Settings.excel_export_dir),
        secret_key=read("SECRET_KEY", Settings.secret_key),
        log_level=read("LOG_LEVEL", Settings.log_level),
        import_batch_size=int(read("IMPORT_BATCH_SIZE", str(Settings.import_batch_size))),
        auth_token_ttl_minutes=int(read("AUTH_TOKEN_TTL_MINUTES", str(Settings.auth_token_ttl_minutes))),
        default_admin_username=read("DEFAULT_ADMIN_USERNAME", Settings.default_admin_username),
        default_admin_password=read("DEFAULT_ADMIN_PASSWORD", Settings.default_admin_password),
    )

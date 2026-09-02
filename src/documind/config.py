from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = ""
    documind_chat_model: str = "gemini-3.7-flash"
    documind_embed_model: str = "gemini-embedding-2"
    documind_data_dir: str = "data"
    documind_collection: str = "documind"
    documind_top_k: int = 6
    documind_max_upload_mb: int = 250
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def data_dir(self) -> Path:
        return Path(self.documind_data_dir)

    @property
    def upload_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def index_dir(self) -> Path:
        return self.data_dir / "index"


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.index_dir.mkdir(parents=True, exist_ok=True)

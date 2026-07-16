from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "FireTV Enhanced Experience API"
    debug: bool = False
    database_url: str = "sqlite:///./firetv.db"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7
    cors_origins: str = "http://localhost:8080,http://localhost:5173,http://localhost:4173"

    # AI providers: heuristic (default, no deps) | onnx | ollama | openrouter
    mood_provider: str = "heuristic"
    onnx_model_path: str = "../research/statement-1/Time_Mood_Behaviour_analysis/Mood_Detection(YOLO)/best.onnx"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.2-3b-instruct:free"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

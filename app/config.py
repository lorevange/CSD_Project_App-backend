from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    openai_api_key: str | None = None
    openai_model: str = "gpt-3.5-turbo"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash-001"


settings = Settings()

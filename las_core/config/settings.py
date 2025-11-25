from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Main Config
    is_local: bool = Field(True, alias="IS_LOCAL")
    provider_name: str = Field("ollama", alias="PROVIDER_NAME")
    provider_model: str = Field("llama3", alias="PROVIDER_MODEL")
    provider_server_address: str = Field("http://127.0.0.1:11434", alias="PROVIDER_SERVER_ADDRESS")
    agent_name: str = Field("Friday", alias="AGENT_NAME")
    recover_last_session: bool = Field(False, alias="RECOVER_LAST_SESSION")
    save_session: bool = Field(False, alias="SAVE_SESSION")
    speak: bool = Field(False, alias="SPEAK")
    listen: bool = Field(False, alias="LISTEN")
    work_dir: str = Field("./workspace", alias="WORK_DIR")
    jarvis_personality: bool = Field(False, alias="JARVIS_PERSONALITY")
    languages: str = Field("en", alias="LANGUAGES")

    # Browser Config
    headless_browser: bool = Field(False, alias="HEADLESS_BROWSER")
    stealth_mode: bool = Field(False, alias="STEALTH_MODE")

    # Ollama Cloud Config
    ollama_cloud_api_key: Optional[str] = Field(None, alias="OLLAMA_CLOUD_API_KEY")

    # Database Config (Future Proofing)
    postgres_user: str = Field("postgres", alias="POSTGRES_USER")
    postgres_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("las_db", alias="POSTGRES_DB")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    # Vector DB Config
    qdrant_host: str = Field("localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(6333, alias="QDRANT_PORT")

    # OpenRouter Config
    app_url: str = Field("https://github.com/your-repo/las", alias="APP_URL")
    app_name: str = Field("Local Agent System", alias="APP_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()

from pydantic import BaseModel, Field
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ENV: str = Field(default="dev")
    LOG_LEVEL: str = Field(default="INFO")
    # Example external API config; replace when switching APIs
    API_BASE_URL: str = Field(default="https://api.publicapis.org")
    API_TIMEOUT_SECS: int = Field(default=15)
    # If the API needs a token later:
    API_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

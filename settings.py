from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./legalease.db"
    AI_API_KEY: str = ""
    AI_MODEL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

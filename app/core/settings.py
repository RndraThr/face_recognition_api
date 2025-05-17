from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    threshold: float = 0.4

    class Config:
        env_file = ".env"

settings = Settings()

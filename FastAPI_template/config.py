from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool
    VERSION: str

    class Config:
        env_file = ".env"
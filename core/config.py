from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TESTING_DATABASE_URL: str

    class Config:
        env_file = ".env"


app_settings = Settings()

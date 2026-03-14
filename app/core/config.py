from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "OCRService"
    ROOT_URL_PREFIX: str = "/api"

    IS_DEV: bool = False


settings = Settings()
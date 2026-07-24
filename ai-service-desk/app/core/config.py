from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Service Desk"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    AWS_SECRET_ACCESS_KEY: str 
    AWS_ACCESS_KEY_ID: str 
    AWS_REGION: str 
    BEDROCK_MODEL_ID: str 
    aws_demo_mode: bool = False
    database_ready: bool = False

    DATABASE_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
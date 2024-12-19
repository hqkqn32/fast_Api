from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    access_token_expire_minutes: int  # Correct name and type
    algorithm:str

    class Config:
        env_file = ".env"


settings=Settings()

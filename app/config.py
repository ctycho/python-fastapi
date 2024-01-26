""" Configuration """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: str = '60'

    class Config:
        env_file = '.env'


settings = Settings()

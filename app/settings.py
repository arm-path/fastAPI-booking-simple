from typing import Literal

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['TEST', 'DEV', 'PROD']
    SITE_NAME: str
    SITE_PROTOCOL: str
    SITE_DOMAIN: str
    SITE_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str

    POSTGRES_HOST_TEST: str
    POSTGRES_PORT_TEST: int
    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str
    POSTGRES_NAME_TEST: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    SECRET_KEY_URL_TOKEN: str
    SECRET_PASSWORD_SALT_URL_TOKEN: str
    SECRET_KEY_ADMIN_AUTH: str

    EMAIL_LOGIN: EmailStr
    EMAIL_PASSWORD: str
    EMAIL_SMTP: str
    EMAIL_PORT: int

    LOG_LEVEL: Literal['INFO', 'WARNING', 'ERROR', 'CRITICAL']

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@' \
               f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}'

    @property
    def TEST_DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER_TEST}:{self.POSTGRES_PASSWORD_TEST}@' \
               f'{self.POSTGRES_HOST_TEST}:{self.POSTGRES_PORT_TEST}/{self.POSTGRES_NAME_TEST}'

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'


settings = Settings()

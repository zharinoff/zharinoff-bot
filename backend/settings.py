from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class App(SettingsBase):
    model_config = SettingsConfigDict(env_prefix="APP_")

    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str


class JWTData(SettingsBase):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class DB(SettingsBase):
    model_config = SettingsConfigDict(env_prefix="DB_")

    ASYNC_PREFIX: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    def get_url(self) -> str:
        return (f"{self.ASYNC_PREFIX}://{self.USER}:{self.PASSWORD}@"
                f"{self.HOST}:{self.PORT}/{self.NAME}")


class VK(SettingsBase):
    model_config = SettingsConfigDict(env_prefix="VK_")

    API_VERSION: str
    GROUP_ID: int
    ADMIN_ID: int
    TOKEN: str


class Settings(BaseSettings):
    app: App = Field(default_factory=App)
    db: DB = Field(default_factory=DB)
    vk: VK = Field(default_factory=VK)

    @classmethod
    def load(cls) -> "Settings":
        return cls()


settings = Settings.load()

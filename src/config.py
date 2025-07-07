from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExampleAppSettings(BaseModel):
    """
    Настройки приложения.
    """

    app_prefix: str = "/example-domain"
    router_prefix: str = "/example-router"


class ApiSettings(BaseModel):
    """
    Настройки API.
    """

    api_prefix: str = "/api"
    v1_prefix: str = "/v1"


class DatabaseSettings(BaseModel):
    """
    Настройки для взаимодействия с базой данных.
    """

    host: str = "from .env"
    port: int = 0000
    name: str = "from .env"
    user: str = "from .env"
    password: str = "from .env"
    echo: bool = True
    echo_pool: bool = True
    pool_size: int = 5  # Количество постоянно открытых соединений
    max_overflow: int = 10  # Количество дополниельных соединений сверх pool_size
    convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        """
        Создаёт url для подключения к базе данных.
        """
        return str(
            PostgresDsn(
                f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
            ),
        )


class Settings(BaseSettings):
    """
    Объедененные настройки.
    """

    app_name: str
    app_port: int
    api: ApiSettings = ApiSettings()
    db: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__",
    )


settings = Settings()

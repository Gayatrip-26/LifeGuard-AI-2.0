from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LifeGuard AI 2.0 Backend"
    app_env: str = "development"
    app_port: int = 8000
    ai_enabled: bool = True

    jwt_secret_key: str = "change-me-use-strong-secret-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    internal_service_token: str = ""

    database_url: str = "postgresql://lifeguard_user:lifeguard_pass@localhost:5432/lifeguard"
    redis_url: str = "redis://localhost:6379/0"
    kafka_bootstrap_servers: str = "localhost:9092"
    chroma_host: str = "localhost"
    chroma_port: int = 8001

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

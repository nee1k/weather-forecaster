"""
Settings configuration for WeatherFlow Analytics.

This module defines all configuration settings using Pydantic for type safety,
validation, and environment variable management.
"""

import os
from typing import List, Optional, Tuple
from pydantic import BaseSettings, Field, validator
from pydantic.types import SecretStr


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    host: str = Field(default="localhost", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    database: str = Field(default="weather_analytics", env="POSTGRES_DB")
    username: str = Field(default="weatherflow", env="POSTGRES_USER")
    password: SecretStr = Field(env="POSTGRES_PASSWORD")
    
    @property
    def url(self) -> str:
        """Get database connection URL."""
        return f"postgresql://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "POSTGRES_"


class KafkaSettings(BaseSettings):
    """Kafka configuration settings."""
    
    bootstrap_servers: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    topic_weather_data: str = Field(default="weather_raw_data", env="KAFKA_TOPIC_WEATHER_DATA")
    topic_processed_data: str = Field(default="weather_processed_data", env="KAFKA_TOPIC_PROCESSED_DATA")
    topic_forecasts: str = Field(default="weather_forecasts", env="KAFKA_TOPIC_FORECASTS")
    topic_alerts: str = Field(default="weather_alerts", env="KAFKA_TOPIC_ALERTS")
    partitions: int = Field(default=3, env="KAFKA_PARTITIONS")
    replication_factor: int = Field(default=1, env="KAFKA_REPLICATION_FACTOR")
    
    class Config:
        env_prefix = "KAFKA_"


class WeatherAPISettings(BaseSettings):
    """Weather API configuration settings."""
    
    api_key: SecretStr = Field(env="WEATHER_API_KEY")
    base_url: str = Field(default="https://api.weatherapi.com/v1", env="WEATHER_API_BASE_URL")
    openweather_api_key: Optional[SecretStr] = Field(default=None, env="OPENWEATHER_API_KEY")
    accuweather_api_key: Optional[SecretStr] = Field(default=None, env="ACCUWEATHER_API_KEY")
    
    class Config:
        env_prefix = "WEATHER_"


class MLSettings(BaseSettings):
    """Machine Learning configuration settings."""
    
    model_retrain_interval: str = Field(default="24h", env="MODEL_RETRAIN_INTERVAL")
    forecast_horizon: int = Field(default=120, env="FORECAST_HORIZON")  # 5 days in hours
    model_confidence_threshold: float = Field(default=0.8, env="MODEL_CONFIDENCE_THRESHOLD")
    sarima_order: Tuple[int, int, int] = Field(default=(1, 1, 1), env="SARIMA_ORDER")
    sarima_seasonal_order: Tuple[int, int, int, int] = Field(default=(1, 1, 1, 24), env="SARIMA_SEASONAL_ORDER")
    
    @validator('sarima_order', 'sarima_seasonal_order', pre=True)
    def parse_tuple(cls, v):
        if isinstance(v, str):
            return eval(v)  # Safe for configuration tuples
        return v
    
    class Config:
        env_prefix = "ML_"


class AirflowSettings(BaseSettings):
    """Apache Airflow configuration settings."""
    
    fernet_key: SecretStr = Field(env="AIRFLOW_FERNET_KEY")
    secret_key: SecretStr = Field(env="AIRFLOW_SECRET_KEY")
    username: str = Field(default="admin", env="AIRFLOW_USERNAME")
    password: SecretStr = Field(env="AIRFLOW_PASSWORD")
    
    class Config:
        env_prefix = "AIRFLOW_"


class APISettings(BaseSettings):
    """API configuration settings."""
    
    secret_key: SecretStr = Field(env="API_SECRET_KEY")
    rate_limit: int = Field(default=1000, env="API_RATE_LIMIT")
    cors_origins: List[str] = Field(default=["http://localhost:8501"], env="API_CORS_ORIGINS")
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    class Config:
        env_prefix = "API_"


class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""
    
    grafana_admin_user: str = Field(default="admin", env="GRAFANA_ADMIN_USER")
    grafana_admin_password: SecretStr = Field(env="GRAFANA_ADMIN_PASSWORD")
    prometheus_retention_days: int = Field(default=30, env="PROMETHEUS_RETENTION_DAYS")
    
    class Config:
        env_prefix = "MONITORING_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(default="json", env="LOG_FORMAT")
    file_path: str = Field(default="/app/logs/weatherflow.log", env="LOG_FILE_PATH")
    
    class Config:
        env_prefix = "LOG_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    enable_ssl: bool = Field(default=False, env="ENABLE_SSL")
    ssl_cert_path: Optional[str] = Field(default=None, env="SSL_CERT_PATH")
    ssl_key_path: Optional[str] = Field(default=None, env="SSL_KEY_PATH")
    
    class Config:
        env_prefix = "SECURITY_"


class PerformanceSettings(BaseSettings):
    """Performance configuration settings."""
    
    spark_worker_memory: str = Field(default="1g", env="SPARK_WORKER_MEMORY")
    spark_worker_cores: int = Field(default=1, env="SPARK_WORKER_CORES")
    data_batch_size: int = Field(default=1000, env="DATA_BATCH_SIZE")
    processing_interval: int = Field(default=300, env="PROCESSING_INTERVAL")  # 5 minutes
    
    class Config:
        env_prefix = "PERFORMANCE_"


class NotificationSettings(BaseSettings):
    """Notification configuration settings."""
    
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[SecretStr] = Field(default=None, env="SMTP_PASSWORD")
    alert_email_recipients: List[str] = Field(default=[], env="ALERT_EMAIL_RECIPIENTS")
    
    @validator('alert_email_recipients', pre=True)
    def parse_email_recipients(cls, v):
        if isinstance(v, str):
            return [email.strip() for email in v.split(',')]
        return v
    
    class Config:
        env_prefix = "NOTIFICATION_"


class DevelopmentSettings(BaseSettings):
    """Development configuration settings."""
    
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="production", env="ENVIRONMENT")
    enable_hot_reload: bool = Field(default=False, env="ENABLE_HOT_RELOAD")
    testing: bool = Field(default=False, env="TESTING")
    
    class Config:
        env_prefix = "DEV_"


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections."""
    
    # Database settings
    database: DatabaseSettings = DatabaseSettings()
    
    # Kafka settings
    kafka: KafkaSettings = KafkaSettings()
    
    # Weather API settings
    weather_api: WeatherAPISettings = WeatherAPISettings()
    
    # Machine Learning settings
    ml: MLSettings = MLSettings()
    
    # Airflow settings
    airflow: AirflowSettings = AirflowSettings()
    
    # API settings
    api: APISettings = APISettings()
    
    # Monitoring settings
    monitoring: MonitoringSettings = MonitoringSettings()
    
    # Logging settings
    logging: LoggingSettings = LoggingSettings()
    
    # Security settings
    security: SecuritySettings = SecuritySettings()
    
    # Performance settings
    performance: PerformanceSettings = PerformanceSettings()
    
    # Notification settings
    notification: NotificationSettings = NotificationSettings()
    
    # Development settings
    development: DevelopmentSettings = DevelopmentSettings()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

"""
Configuration management for WeatherFlow Analytics.

This module provides centralized configuration management using Pydantic settings
for type safety and validation.
"""

from .settings import Settings

# Global settings instance
settings = Settings()

__all__ = ["settings", "Settings"]

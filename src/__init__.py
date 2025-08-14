"""
WeatherFlow Analytics - Advanced Weather Forecasting Platform

A comprehensive data engineering platform for real-time weather data processing,
machine learning-based forecasting, and interactive visualizations.

Author: WeatherFlow Analytics Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "WeatherFlow Analytics Team"
__email__ = "support@weatherflow-analytics.com"

from .config import settings
from .utils.logging import setup_logging

# Setup logging configuration
setup_logging()

__all__ = [
    "settings",
    "setup_logging",
]

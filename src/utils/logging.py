"""
Logging configuration for WeatherFlow Analytics.

This module provides structured logging with JSON formatting, multiple handlers,
and configurable log levels for different environments.
"""

import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..config.settings import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format the message
        formatted = super().format(record)
        
        # Add color to level name
        formatted = formatted.replace(
            record.levelname,
            f"{color}{record.levelname}{reset}"
        )
        
        return formatted


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format (json, colored, simple)
        log_file: Path to log file
    """
    # Get configuration from settings
    config = settings.logging
    log_level = log_level or config.level
    log_format = log_format or config.format
    log_file = log_file or config.file_path
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    if log_format == "json":
        console_formatter = JSONFormatter()
    elif log_format == "colored":
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        console_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if log file is specified)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        if log_format == "json":
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("kafka").setLevel(logging.INFO)
    logging.getLogger("confluent_kafka").setLevel(logging.INFO)
    logging.getLogger("airflow").setLevel(logging.INFO)
    
    # Log startup message
    logger = get_logger(__name__)
    logger.info(
        "Logging configured successfully",
        extra={
            "extra_fields": {
                "log_level": log_level,
                "log_format": log_format,
                "log_file": log_file,
                "environment": settings.development.environment
            }
        }
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **context: Any
) -> None:
    """
    Log a message with additional context.
    
    Args:
        logger: Logger instance
        level: Log level
        message: Log message
        **context: Additional context fields
    """
    extra_fields = {"extra_fields": context}
    
    if level.upper() == "DEBUG":
        logger.debug(message, extra=extra_fields)
    elif level.upper() == "INFO":
        logger.info(message, extra=extra_fields)
    elif level.upper() == "WARNING":
        logger.warning(message, extra=extra_fields)
    elif level.upper() == "ERROR":
        logger.error(message, extra=extra_fields)
    elif level.upper() == "CRITICAL":
        logger.critical(message, extra=extra_fields)
    else:
        logger.info(message, extra=extra_fields)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    def log_info(self, message: str, **context: Any) -> None:
        """Log info message with context."""
        log_with_context(self.logger, "INFO", message, **context)
    
    def log_warning(self, message: str, **context: Any) -> None:
        """Log warning message with context."""
        log_with_context(self.logger, "WARNING", message, **context)
    
    def log_error(self, message: str, **context: Any) -> None:
        """Log error message with context."""
        log_with_context(self.logger, "ERROR", message, **context)
    
    def log_debug(self, message: str, **context: Any) -> None:
        """Log debug message with context."""
        log_with_context(self.logger, "DEBUG", message, **context)

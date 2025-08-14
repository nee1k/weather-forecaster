"""
Weather data models for WeatherFlow Analytics.

This module defines Pydantic models for weather data structures including
current weather, forecasts, and alerts with comprehensive validation.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum


class WeatherCondition(str, Enum):
    """Weather condition types."""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAIN = "rain"
    SNOW = "snow"
    STORM = "storm"
    FOG = "fog"
    WINDY = "windy"
    PARTLY_CLOUDY = "partly_cloudy"
    OVERCAST = "overcast"
    DRIZZLE = "drizzle"
    THUNDERSTORM = "thunderstorm"
    HAIL = "hail"
    SLEET = "sleet"
    MIST = "mist"
    UNKNOWN = "unknown"


class WindDirection(str, Enum):
    """Wind direction types."""
    NORTH = "N"
    NORTH_EAST = "NE"
    EAST = "E"
    SOUTH_EAST = "SE"
    SOUTH = "S"
    SOUTH_WEST = "SW"
    WEST = "W"
    NORTH_WEST = "NW"


class AlertSeverity(str, Enum):
    """Weather alert severity levels."""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"


class WeatherData(BaseModel):
    """Model for current weather data."""
    
    # Location information
    location: str = Field(..., description="Location name")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp")
    
    # Temperature data
    temperature: float = Field(..., ge=-100, le=100, description="Temperature in Celsius")
    feels_like: Optional[float] = Field(None, ge=-100, le=100, description="Feels like temperature")
    temperature_min: Optional[float] = Field(None, ge=-100, le=100, description="Minimum temperature")
    temperature_max: Optional[float] = Field(None, ge=-100, le=100, description="Maximum temperature")
    
    # Humidity and pressure
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Humidity percentage")
    pressure: Optional[float] = Field(None, ge=800, le=1200, description="Atmospheric pressure in hPa")
    
    # Wind data
    wind_speed: Optional[float] = Field(None, ge=0, description="Wind speed in km/h")
    wind_direction: Optional[WindDirection] = Field(None, description="Wind direction")
    wind_gust: Optional[float] = Field(None, ge=0, description="Wind gust speed in km/h")
    
    # Precipitation
    precipitation: Optional[float] = Field(None, ge=0, description="Precipitation amount in mm")
    precipitation_probability: Optional[float] = Field(None, ge=0, le=1, description="Precipitation probability")
    
    # Visibility and clouds
    visibility: Optional[float] = Field(None, ge=0, le=50, description="Visibility in km")
    cloud_cover: Optional[float] = Field(None, ge=0, le=100, description="Cloud cover percentage")
    
    # Weather condition
    condition: WeatherCondition = Field(..., description="Weather condition")
    condition_description: Optional[str] = Field(None, description="Human-readable condition description")
    
    # UV and solar data
    uv_index: Optional[float] = Field(None, ge=0, le=15, description="UV index")
    solar_radiation: Optional[float] = Field(None, ge=0, description="Solar radiation in W/m²")
    
    # Additional metadata
    source: str = Field(default="weather_api", description="Data source")
    quality_score: Optional[float] = Field(None, ge=0, le=1, description="Data quality score")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "location": "Bloomington, Indiana",
                "latitude": 39.1653,
                "longitude": -86.5264,
                "timestamp": "2024-04-24T10:30:00Z",
                "temperature": 22.5,
                "feels_like": 24.2,
                "humidity": 65,
                "pressure": 1013.25,
                "wind_speed": 8.5,
                "wind_direction": "SW",
                "precipitation": 0.0,
                "precipitation_probability": 0.1,
                "visibility": 10.0,
                "cloud_cover": 30,
                "condition": "partly_cloudy",
                "condition_description": "Partly cloudy",
                "uv_index": 5.2,
                "source": "weather_api",
                "quality_score": 0.95
            }
        }
    
    @validator('temperature', 'feels_like', 'temperature_min', 'temperature_max')
    def validate_temperature_range(cls, v):
        """Validate temperature is within reasonable range."""
        if v is not None and (v < -100 or v > 100):
            raise ValueError('Temperature must be between -100 and 100 degrees Celsius')
        return v
    
    @validator('humidity')
    def validate_humidity(cls, v):
        """Validate humidity is within valid range."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Humidity must be between 0 and 100 percent')
        return v
    
    @validator('pressure')
    def validate_pressure(cls, v):
        """Validate atmospheric pressure is within reasonable range."""
        if v is not None and (v < 800 or v > 1200):
            raise ValueError('Pressure must be between 800 and 1200 hPa')
        return v
    
    @root_validator
    def validate_temperature_consistency(cls, values):
        """Validate temperature consistency."""
        temp = values.get('temperature')
        temp_min = values.get('temperature_min')
        temp_max = values.get('temperature_max')
        
        if temp_min is not None and temp_max is not None and temp_min > temp_max:
            raise ValueError('Minimum temperature cannot be greater than maximum temperature')
        
        if temp is not None:
            if temp_min is not None and temp < temp_min:
                raise ValueError('Current temperature cannot be less than minimum temperature')
            if temp_max is not None and temp > temp_max:
                raise ValueError('Current temperature cannot be greater than maximum temperature')
        
        return values


class WeatherForecast(BaseModel):
    """Model for weather forecast data."""
    
    location: str = Field(..., description="Location name")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    
    # Forecast period
    forecast_date: datetime = Field(..., description="Forecast date")
    forecast_horizon: int = Field(..., ge=1, le=240, description="Forecast horizon in hours")
    
    # Temperature forecast
    temperature_high: float = Field(..., ge=-100, le=100, description="High temperature")
    temperature_low: float = Field(..., ge=-100, le=100, description="Low temperature")
    temperature_avg: Optional[float] = Field(None, ge=-100, le=100, description="Average temperature")
    
    # Weather conditions
    condition: WeatherCondition = Field(..., description="Weather condition")
    condition_description: Optional[str] = Field(None, description="Condition description")
    
    # Precipitation forecast
    precipitation_probability: float = Field(..., ge=0, le=1, description="Precipitation probability")
    precipitation_amount: Optional[float] = Field(None, ge=0, description="Expected precipitation in mm")
    
    # Wind forecast
    wind_speed: Optional[float] = Field(None, ge=0, description="Wind speed in km/h")
    wind_direction: Optional[WindDirection] = Field(None, description="Wind direction")
    
    # Additional forecast data
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Humidity percentage")
    uv_index: Optional[float] = Field(None, ge=0, le=15, description="UV index")
    
    # Model information
    model_confidence: float = Field(..., ge=0, le=1, description="Model confidence score")
    model_version: str = Field(default="1.0.0", description="Model version used")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Forecast generation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "location": "Bloomington, Indiana",
                "latitude": 39.1653,
                "longitude": -86.5264,
                "forecast_date": "2024-04-25T00:00:00Z",
                "forecast_horizon": 24,
                "temperature_high": 25.0,
                "temperature_low": 15.0,
                "temperature_avg": 20.0,
                "condition": "partly_cloudy",
                "condition_description": "Partly cloudy with occasional sunshine",
                "precipitation_probability": 0.2,
                "precipitation_amount": 2.5,
                "wind_speed": 12.0,
                "wind_direction": "SW",
                "humidity": 70,
                "uv_index": 6.0,
                "model_confidence": 0.85,
                "model_version": "1.0.0",
                "generated_at": "2024-04-24T10:30:00Z"
            }
        }
    
    @validator('temperature_high', 'temperature_low', 'temperature_avg')
    def validate_temperature_range(cls, v):
        """Validate temperature is within reasonable range."""
        if v is not None and (v < -100 or v > 100):
            raise ValueError('Temperature must be between -100 and 100 degrees Celsius')
        return v
    
    @root_validator
    def validate_temperature_consistency(cls, values):
        """Validate temperature consistency."""
        temp_high = values.get('temperature_high')
        temp_low = values.get('temperature_low')
        
        if temp_high is not None and temp_low is not None and temp_low > temp_high:
            raise ValueError('Low temperature cannot be greater than high temperature')
        
        return values


class WeatherAlert(BaseModel):
    """Model for weather alerts and warnings."""
    
    alert_id: str = Field(..., description="Unique alert identifier")
    location: str = Field(..., description="Alert location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    
    # Alert details
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    severity: AlertSeverity = Field(..., description="Alert severity level")
    
    # Timing
    issued_at: datetime = Field(..., description="Alert issuance timestamp")
    effective_from: datetime = Field(..., description="Alert effective from")
    effective_until: datetime = Field(..., description="Alert effective until")
    
    # Alert type and category
    alert_type: str = Field(..., description="Type of weather alert")
    category: Optional[str] = Field(None, description="Alert category")
    
    # Additional information
    instructions: Optional[str] = Field(None, description="Safety instructions")
    source: str = Field(default="weather_api", description="Alert source")
    is_active: bool = Field(default=True, description="Whether alert is currently active")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "alert_id": "WX123456",
                "location": "Bloomington, Indiana",
                "latitude": 39.1653,
                "longitude": -86.5264,
                "title": "Severe Thunderstorm Warning",
                "description": "Severe thunderstorms with heavy rain and strong winds expected",
                "severity": "severe",
                "issued_at": "2024-04-24T15:00:00Z",
                "effective_from": "2024-04-24T15:00:00Z",
                "effective_until": "2024-04-24T18:00:00Z",
                "alert_type": "thunderstorm_warning",
                "category": "severe_weather",
                "instructions": "Seek shelter immediately. Avoid outdoor activities.",
                "source": "weather_api",
                "is_active": True
            }
        }
    
    @root_validator
    def validate_timing(cls, values):
        """Validate alert timing consistency."""
        issued_at = values.get('issued_at')
        effective_from = values.get('effective_from')
        effective_until = values.get('effective_until')
        
        if effective_from and effective_until and effective_from >= effective_until:
            raise ValueError('Effective from time must be before effective until time')
        
        if issued_at and effective_from and issued_at > effective_from:
            raise ValueError('Issued at time cannot be after effective from time')
        
        return values


class WeatherDataBatch(BaseModel):
    """Model for batch weather data processing."""
    
    batch_id: str = Field(..., description="Unique batch identifier")
    records: List[WeatherData] = Field(..., description="List of weather data records")
    total_records: int = Field(..., description="Total number of records")
    batch_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Batch timestamp")
    source: str = Field(default="weather_api", description="Data source")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @validator('total_records')
    def validate_total_records(cls, v, values):
        """Validate total records matches actual records count."""
        if 'records' in values and v != len(values['records']):
            raise ValueError('Total records count must match actual records count')
        return v


class ForecastBatch(BaseModel):
    """Model for batch forecast data."""
    
    batch_id: str = Field(..., description="Unique batch identifier")
    location: str = Field(..., description="Location name")
    forecasts: List[WeatherForecast] = Field(..., description="List of weather forecasts")
    forecast_period: str = Field(..., description="Forecast period (e.g., '5-day')")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    model_version: str = Field(default="1.0.0", description="Model version used")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

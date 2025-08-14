-- ============================================================================
-- WeatherFlow Analytics - Database Schema
-- ============================================================================
-- Initial database schema for weather data storage and analytics

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

-- Weather condition types
CREATE TYPE weather_condition AS ENUM (
    'clear', 'cloudy', 'rain', 'snow', 'storm', 'fog', 'windy',
    'partly_cloudy', 'overcast', 'drizzle', 'thunderstorm',
    'hail', 'sleet', 'mist', 'unknown'
);

-- Wind direction types
CREATE TYPE wind_direction AS ENUM (
    'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'
);

-- Alert severity levels
CREATE TYPE alert_severity AS ENUM (
    'minor', 'moderate', 'severe', 'extreme'
);

-- ============================================================================
-- WEATHER DATA TABLES
-- ============================================================================

-- Current weather data table
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location VARCHAR(255) NOT NULL,
    latitude DECIMAL(8, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Temperature data
    temperature DECIMAL(4, 1) NOT NULL,
    feels_like DECIMAL(4, 1),
    temperature_min DECIMAL(4, 1),
    temperature_max DECIMAL(4, 1),
    
    -- Humidity and pressure
    humidity INTEGER CHECK (humidity >= 0 AND humidity <= 100),
    pressure DECIMAL(6, 2) CHECK (pressure >= 800 AND pressure <= 1200),
    
    -- Wind data
    wind_speed DECIMAL(5, 2),
    wind_direction wind_direction,
    wind_gust DECIMAL(5, 2),
    
    -- Precipitation
    precipitation DECIMAL(6, 2),
    precipitation_probability DECIMAL(3, 2) CHECK (precipitation_probability >= 0 AND precipitation_probability <= 1),
    
    -- Visibility and clouds
    visibility DECIMAL(4, 1) CHECK (visibility >= 0 AND visibility <= 50),
    cloud_cover INTEGER CHECK (cloud_cover >= 0 AND cloud_cover <= 100),
    
    -- Weather condition
    condition weather_condition NOT NULL,
    condition_description TEXT,
    
    -- UV and solar data
    uv_index DECIMAL(3, 1) CHECK (uv_index >= 0 AND uv_index <= 15),
    solar_radiation DECIMAL(6, 2),
    
    -- Metadata
    source VARCHAR(100) DEFAULT 'weather_api',
    quality_score DECIMAL(3, 2) CHECK (quality_score >= 0 AND quality_score <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather forecasts table
CREATE TABLE weather_forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location VARCHAR(255) NOT NULL,
    latitude DECIMAL(8, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    forecast_date TIMESTAMP WITH TIME ZONE NOT NULL,
    forecast_horizon INTEGER NOT NULL CHECK (forecast_horizon >= 1 AND forecast_horizon <= 240),
    
    -- Temperature forecast
    temperature_high DECIMAL(4, 1) NOT NULL,
    temperature_low DECIMAL(4, 1) NOT NULL,
    temperature_avg DECIMAL(4, 1),
    
    -- Weather conditions
    condition weather_condition NOT NULL,
    condition_description TEXT,
    
    -- Precipitation forecast
    precipitation_probability DECIMAL(3, 2) NOT NULL CHECK (precipitation_probability >= 0 AND precipitation_probability <= 1),
    precipitation_amount DECIMAL(6, 2),
    
    -- Wind forecast
    wind_speed DECIMAL(5, 2),
    wind_direction wind_direction,
    
    -- Additional forecast data
    humidity INTEGER CHECK (humidity >= 0 AND humidity <= 100),
    uv_index DECIMAL(3, 1) CHECK (uv_index >= 0 AND uv_index <= 15),
    
    -- Model information
    model_confidence DECIMAL(3, 2) NOT NULL CHECK (model_confidence >= 0 AND model_confidence <= 1),
    model_version VARCHAR(50) DEFAULT '1.0.0',
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT temperature_consistency CHECK (temperature_low <= temperature_high),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather alerts table
CREATE TABLE weather_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id VARCHAR(100) UNIQUE NOT NULL,
    location VARCHAR(255) NOT NULL,
    latitude DECIMAL(8, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    
    -- Alert details
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    severity alert_severity NOT NULL,
    
    -- Timing
    issued_at TIMESTAMP WITH TIME ZONE NOT NULL,
    effective_from TIMESTAMP WITH TIME ZONE NOT NULL,
    effective_until TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Alert type and category
    alert_type VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    
    -- Additional information
    instructions TEXT,
    source VARCHAR(100) DEFAULT 'weather_api',
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Constraints
    CONSTRAINT alert_timing CHECK (effective_from < effective_until),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- MACHINE LEARNING TABLES
-- ============================================================================

-- Model metadata table
CREATE TABLE ml_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    model_type VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    
    -- Model parameters
    parameters JSONB,
    hyperparameters JSONB,
    
    -- Performance metrics
    accuracy DECIMAL(5, 4),
    mae DECIMAL(6, 4),  -- Mean Absolute Error
    rmse DECIMAL(6, 4), -- Root Mean Square Error
    mape DECIMAL(6, 4), -- Mean Absolute Percentage Error
    
    -- Model files
    model_path VARCHAR(500),
    scaler_path VARCHAR(500),
    
    -- Status
    is_active BOOLEAN DEFAULT FALSE,
    is_production BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(model_name, model_version, location)
);

-- Model training history
CREATE TABLE ml_training_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID REFERENCES ml_models(id) ON DELETE CASCADE,
    
    -- Training metrics
    training_accuracy DECIMAL(5, 4),
    validation_accuracy DECIMAL(5, 4),
    training_loss DECIMAL(8, 6),
    validation_loss DECIMAL(8, 6),
    
    -- Training parameters
    epochs INTEGER,
    batch_size INTEGER,
    learning_rate DECIMAL(10, 8),
    
    -- Training duration
    training_duration_seconds INTEGER,
    
    -- Status
    status VARCHAR(50) DEFAULT 'completed',
    error_message TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- DATA QUALITY TABLES
-- ============================================================================

-- Data quality metrics
CREATE TABLE data_quality_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(255) NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(10, 4),
    metric_threshold DECIMAL(10, 4),
    is_passed BOOLEAN,
    
    -- Context
    record_count INTEGER,
    error_count INTEGER,
    null_count INTEGER,
    
    -- Timing
    check_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Data quality alerts
CREATE TABLE data_quality_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    
    -- Status
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SYSTEM TABLES
-- ============================================================================

-- API usage tracking
CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    user_agent TEXT,
    ip_address INET,
    response_time_ms INTEGER,
    status_code INTEGER,
    error_message TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System events
CREATE TABLE system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    event_level VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    details JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES
-- ============================================================================

-- Weather data indexes
CREATE INDEX idx_weather_data_location ON weather_data(location);
CREATE INDEX idx_weather_data_timestamp ON weather_data(timestamp);
CREATE INDEX idx_weather_data_location_timestamp ON weather_data(location, timestamp);
CREATE INDEX idx_weather_data_coordinates ON weather_data(latitude, longitude);
CREATE INDEX idx_weather_data_condition ON weather_data(condition);
CREATE INDEX idx_weather_data_source ON weather_data(source);

-- Weather forecasts indexes
CREATE INDEX idx_weather_forecasts_location ON weather_forecasts(location);
CREATE INDEX idx_weather_forecasts_date ON weather_forecasts(forecast_date);
CREATE INDEX idx_weather_forecasts_location_date ON weather_forecasts(location, forecast_date);
CREATE INDEX idx_weather_forecasts_horizon ON weather_forecasts(forecast_horizon);
CREATE INDEX idx_weather_forecasts_model_version ON weather_forecasts(model_version);

-- Weather alerts indexes
CREATE INDEX idx_weather_alerts_location ON weather_alerts(location);
CREATE INDEX idx_weather_alerts_severity ON weather_alerts(severity);
CREATE INDEX idx_weather_alerts_effective_from ON weather_alerts(effective_from);
CREATE INDEX idx_weather_alerts_effective_until ON weather_alerts(effective_until);
CREATE INDEX idx_weather_alerts_active ON weather_alerts(is_active);
CREATE INDEX idx_weather_alerts_type ON weather_alerts(alert_type);

-- ML models indexes
CREATE INDEX idx_ml_models_name_version ON ml_models(model_name, model_version);
CREATE INDEX idx_ml_models_location ON ml_models(location);
CREATE INDEX idx_ml_models_active ON ml_models(is_active);
CREATE INDEX idx_ml_models_production ON ml_models(is_production);

-- Data quality indexes
CREATE INDEX idx_data_quality_metrics_table_date ON data_quality_metrics(table_name, check_date);
CREATE INDEX idx_data_quality_alerts_table ON data_quality_alerts(table_name);
CREATE INDEX idx_data_quality_alerts_resolved ON data_quality_alerts(is_resolved);

-- API usage indexes
CREATE INDEX idx_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX idx_api_usage_created_at ON api_usage(created_at);
CREATE INDEX idx_api_usage_status_code ON api_usage(status_code);

-- System events indexes
CREATE INDEX idx_system_events_type ON system_events(event_type);
CREATE INDEX idx_system_events_level ON system_events(event_level);
CREATE INDEX idx_system_events_created_at ON system_events(created_at);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_weather_data_updated_at BEFORE UPDATE ON weather_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_weather_forecasts_updated_at BEFORE UPDATE ON weather_forecasts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_weather_alerts_updated_at BEFORE UPDATE ON weather_alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ml_models_updated_at BEFORE UPDATE ON ml_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_data_quality_alerts_updated_at BEFORE UPDATE ON data_quality_alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Current weather view
CREATE VIEW current_weather AS
SELECT 
    location,
    latitude,
    longitude,
    temperature,
    feels_like,
    humidity,
    pressure,
    wind_speed,
    wind_direction,
    condition,
    condition_description,
    uv_index,
    timestamp,
    source
FROM weather_data
WHERE timestamp = (
    SELECT MAX(timestamp) 
    FROM weather_data w2 
    WHERE w2.location = weather_data.location
);

-- Latest forecasts view
CREATE VIEW latest_forecasts AS
SELECT 
    location,
    latitude,
    longitude,
    forecast_date,
    forecast_horizon,
    temperature_high,
    temperature_low,
    temperature_avg,
    condition,
    precipitation_probability,
    precipitation_amount,
    wind_speed,
    wind_direction,
    humidity,
    uv_index,
    model_confidence,
    model_version,
    generated_at
FROM weather_forecasts
WHERE (location, forecast_date) IN (
    SELECT location, MAX(forecast_date)
    FROM weather_forecasts
    GROUP BY location
);

-- Active alerts view
CREATE VIEW active_alerts AS
SELECT 
    alert_id,
    location,
    latitude,
    longitude,
    title,
    description,
    severity,
    alert_type,
    category,
    instructions,
    issued_at,
    effective_from,
    effective_until
FROM weather_alerts
WHERE is_active = TRUE 
  AND effective_from <= CURRENT_TIMESTAMP 
  AND effective_until >= CURRENT_TIMESTAMP;

-- ============================================================================
-- GRANTS
-- ============================================================================

-- Grant permissions to weatherflow user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO weatherflow;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO weatherflow;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO weatherflow;

-- Grant permissions to views
GRANT SELECT ON current_weather TO weatherflow;
GRANT SELECT ON latest_forecasts TO weatherflow;
GRANT SELECT ON active_alerts TO weatherflow;

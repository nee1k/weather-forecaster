# WeatherFlow Analytics 🌤️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7+-orange.svg)](https://airflow.apache.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-3.0+-black.svg)](https://kafka.apache.org/)

> **Advanced Weather Forecasting Platform with Real-time Data Processing and Machine Learning**

WeatherFlow Analytics is a comprehensive, production-ready weather forecasting platform that leverages cutting-edge data engineering technologies to provide accurate 5-day weather predictions. Built with Apache Kafka for real-time data streaming, Apache Spark for distributed processing, and advanced machine learning models for predictive analytics.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│   Apache Kafka  │───▶│  Apache Spark   │
│   (Weather APIs)│    │   (Streaming)   │    │  (Processing)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │◀───│  Apache Airflow │◀───│   ML Models     │
│   (Storage)     │    │  (Orchestration)│    │  (SARIMA/LSTM)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │◀───│   Web Dashboard │◀───│   Predictions   │
│   (Prometheus)  │    │   (Streamlit)   │    │   (API)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Key Features

- **Real-time Data Streaming**: Apache Kafka for high-throughput weather data ingestion
- **Distributed Processing**: Apache Spark for scalable data transformation and analytics
- **Advanced ML Models**: SARIMA and LSTM models for accurate weather forecasting
- **Workflow Orchestration**: Apache Airflow for reliable pipeline management
- **Interactive Dashboard**: Real-time weather visualizations and predictions
- **Production Monitoring**: Comprehensive logging, metrics, and alerting
- **Containerized Deployment**: Docker-based microservices architecture
- **Scalable Infrastructure**: Kubernetes-ready deployment configurations

## 📋 Prerequisites

- **Docker & Docker Compose** (v20.10+)
- **Python** (3.9+)
- **Git** (2.30+)
- **8GB+ RAM** (recommended for local development)
- **20GB+ Disk Space**

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/weatherflow-analytics.git
cd weatherflow-analytics
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Start the Platform

```bash
# Start all services
make up

# Or start individual components
make kafka-up
make spark-up
make airflow-up
make postgres-up
```

### 4. Access Services

| Service | URL | Description |
|---------|-----|-------------|
| **Airflow UI** | http://localhost:8080 | Workflow orchestration dashboard |
| **Kafka Control Center** | http://localhost:9021 | Kafka cluster monitoring |
| **Weather Dashboard** | http://localhost:8501 | Interactive weather visualizations |
| **PostgreSQL** | localhost:5432 | Database (user: weatherflow, db: weather_analytics) |
| **Prometheus** | http://localhost:9090 | Metrics monitoring |
| **Grafana** | http://localhost:3000 | Advanced monitoring dashboards |

## 📊 Data Pipeline

### 1. Data Ingestion
- **Real-time weather data** from multiple APIs
- **Historical data** from weather databases
- **Sensor data** from IoT devices (future enhancement)

### 2. Data Processing
- **Data validation** and quality checks
- **Feature engineering** for ML models
- **Real-time aggregation** and windowing

### 3. Machine Learning
- **SARIMA models** for seasonal forecasting
- **LSTM networks** for complex pattern recognition
- **Ensemble methods** for improved accuracy

### 4. Data Storage
- **PostgreSQL** for structured weather data
- **Time-series optimization** for historical data
- **Real-time analytics** capabilities

## 🔧 Configuration

### Environment Variables

```bash
# Database Configuration
POSTGRES_DB=weather_analytics
POSTGRES_USER=weatherflow
POSTGRES_PASSWORD=secure_password

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_WEATHER_DATA=weather_raw_data
KAFKA_TOPIC_PROCESSED_DATA=weather_processed_data

# API Configuration
WEATHER_API_KEY=your_api_key_here
WEATHER_API_BASE_URL=https://api.weatherapi.com/v1

# ML Model Configuration
MODEL_RETRAIN_INTERVAL=24h
FORECAST_HORIZON=120  # 5 days in hours
```

### Airflow DAGs

The platform includes several DAGs for different workflows:

- **`weather_data_ingestion`**: Real-time data collection
- **`weather_data_processing`**: Data transformation and feature engineering
- **`ml_model_training`**: Automated model retraining
- **`weather_forecasting`**: Daily forecast generation
- **`data_quality_monitoring`**: Data quality checks and alerts

## 📈 Monitoring & Observability

### Metrics Collection
- **Prometheus** for time-series metrics
- **Grafana** for visualization and alerting
- **Custom metrics** for business KPIs

### Logging
- **Structured logging** with JSON format
- **Centralized log aggregation** (ELK stack ready)
- **Log retention policies** for compliance

### Health Checks
- **Service health endpoints** for all components
- **Automated alerting** for service failures
- **Performance monitoring** and optimization

## 🔒 Security

- **SSL/TLS encryption** for all communications
- **Authentication** and authorization for all services
- **Secrets management** with environment variables
- **Network isolation** with Docker networks
- **Regular security updates** and vulnerability scanning

## 🧪 Testing

```bash
# Run unit tests
make test

# Run integration tests
make test-integration

# Run end-to-end tests
make test-e2e

# Generate test coverage report
make coverage
```

## 📚 API Documentation

### Weather Forecast API

```bash
# Get current weather
GET /api/v1/weather/current?location=bloomington,indiana

# Get 5-day forecast
GET /api/v1/weather/forecast?location=bloomington,indiana&days=5

# Get historical data
GET /api/v1/weather/historical?location=bloomington,indiana&start_date=2024-01-01&end_date=2024-01-31
```

### Response Format

```json
{
  "location": "Bloomington, Indiana",
  "timestamp": "2024-04-24T10:30:00Z",
  "forecast": [
    {
      "date": "2024-04-25",
      "temperature_high": 72.5,
      "temperature_low": 58.2,
      "precipitation_probability": 0.15,
      "wind_speed": 8.5,
      "humidity": 65
    }
  ],
  "model_confidence": 0.89,
  "last_updated": "2024-04-24T10:30:00Z"
}
```

## 🚀 Deployment

### Local Development

```bash
# Start development environment
make dev

# Run with hot reload
make dev-watch
```

### Production Deployment

```bash
# Build production images
make build-prod

# Deploy to production
make deploy-prod

# Scale services
make scale-kafka=3
make scale-spark=2
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Monitor deployment
kubectl get pods -n weatherflow
```
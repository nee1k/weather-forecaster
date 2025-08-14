# WeatherFlow Analytics - Makefile
# Production-ready data engineering platform

.PHONY: help up down build clean test lint format docker-build docker-push
.PHONY: kafka-up kafka-down spark-up spark-down airflow-up airflow-down postgres-up postgres-down
.PHONY: dev dev-watch logs monitor dashboard api-docs

# Default target
help: ## Show this help message
	@echo "WeatherFlow Analytics - Production Data Engineering Platform"
	@echo "=========================================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Environment setup
setup: ## Initial project setup
	@echo "Setting up WeatherFlow Analytics..."
	cp .env.example .env
	@echo "✅ Environment file created. Please edit .env with your configuration."
	@echo "📝 Next steps:"
	@echo "   1. Edit .env file with your API keys and configuration"
	@echo "   2. Run 'make build' to build Docker images"
	@echo "   3. Run 'make up' to start all services"

# Docker operations
build: ## Build all Docker images
	@echo "🔨 Building Docker images..."
	docker-compose -f docker-compose.yml build
	@echo "✅ All images built successfully"

up: ## Start all services
	@echo "🚀 Starting WeatherFlow Analytics platform..."
	docker-compose -f docker-compose.yml up -d
	@echo "✅ All services started"
	@echo "📊 Access services:"
	@echo "   - Airflow UI: http://localhost:8080"
	@echo "   - Kafka Control Center: http://localhost:9021"
	@echo "   - Weather Dashboard: http://localhost:8501"
	@echo "   - PostgreSQL: localhost:5432"
	@echo "   - Prometheus: http://localhost:9090"
	@echo "   - Grafana: http://localhost:3000"

down: ## Stop all services
	@echo "🛑 Stopping all services..."
	docker-compose -f docker-compose.yml down
	@echo "✅ All services stopped"

restart: down up ## Restart all services

# Individual service management
kafka-up: ## Start Kafka cluster
	@echo "📡 Starting Kafka cluster..."
	docker-compose -f docker-compose.yml up -d zookeeper broker schema-registry connect control-center
	@echo "✅ Kafka cluster started"

kafka-down: ## Stop Kafka cluster
	@echo "📡 Stopping Kafka cluster..."
	docker-compose -f docker-compose.yml stop zookeeper broker schema-registry connect control-center
	@echo "✅ Kafka cluster stopped"

spark-up: ## Start Spark cluster
	@echo "⚡ Starting Spark cluster..."
	docker-compose -f docker-compose.yml up -d spark-master spark-worker
	@echo "✅ Spark cluster started"

spark-down: ## Stop Spark cluster
	@echo "⚡ Stopping Spark cluster..."
	docker-compose -f docker-compose.yml stop spark-master spark-worker
	@echo "✅ Spark cluster stopped"

airflow-up: ## Start Airflow
	@echo "🌪️ Starting Airflow..."
	docker-compose -f docker-compose.yml up -d airflow-webserver airflow-scheduler
	@echo "✅ Airflow started"

airflow-down: ## Stop Airflow
	@echo "🌪️ Stopping Airflow..."
	docker-compose -f docker-compose.yml stop airflow-webserver airflow-scheduler
	@echo "✅ Airflow stopped"

postgres-up: ## Start PostgreSQL
	@echo "🗄️ Starting PostgreSQL..."
	docker-compose -f docker-compose.yml up -d postgres
	@echo "✅ PostgreSQL started"

postgres-down: ## Stop PostgreSQL
	@echo "🗄️ Stopping PostgreSQL..."
	docker-compose -f docker-compose.yml stop postgres
	@echo "✅ PostgreSQL stopped"

# Development
dev: ## Start development environment
	@echo "🔧 Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started"

dev-watch: ## Start development with hot reload
	@echo "🔧 Starting development with hot reload..."
	docker-compose -f docker-compose.dev.yml up
	@echo "✅ Development environment with hot reload started"

# Monitoring and logs
logs: ## Show logs from all services
	docker-compose -f docker-compose.yml logs -f

logs-kafka: ## Show Kafka logs
	docker-compose -f docker-compose.yml logs -f zookeeper broker schema-registry connect control-center

logs-airflow: ## Show Airflow logs
	docker-compose -f docker-compose.yml logs -f airflow-webserver airflow-scheduler

logs-spark: ## Show Spark logs
	docker-compose -f docker-compose.yml logs -f spark-master spark-worker

logs-postgres: ## Show PostgreSQL logs
	docker-compose -f docker-compose.yml logs -f postgres

# Testing
test: ## Run all tests
	@echo "🧪 Running tests..."
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
	@echo "✅ Tests completed"

test-unit: ## Run unit tests
	@echo "🧪 Running unit tests..."
	docker-compose -f docker-compose.test.yml run --rm app python -m pytest tests/unit/ -v

test-integration: ## Run integration tests
	@echo "🧪 Running integration tests..."
	docker-compose -f docker-compose.test.yml run --rm app python -m pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests
	@echo "🧪 Running end-to-end tests..."
	docker-compose -f docker-compose.test.yml run --rm app python -m pytest tests/e2e/ -v

coverage: ## Generate test coverage report
	@echo "📊 Generating coverage report..."
	docker-compose -f docker-compose.test.yml run --rm app python -m pytest --cov=src --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated"

# Code quality
lint: ## Run linting
	@echo "🔍 Running linting..."
	docker-compose -f docker-compose.test.yml run --rm app flake8 src/ tests/
	@echo "✅ Linting completed"

format: ## Format code
	@echo "🎨 Formatting code..."
	docker-compose -f docker-compose.test.yml run --rm app black src/ tests/
	@echo "✅ Code formatting completed"

# Database operations
db-migrate: ## Run database migrations
	@echo "🗄️ Running database migrations..."
	docker-compose -f docker-compose.yml exec postgres psql -U weatherflow -d weather_analytics -f /docker-entrypoint-initdb.d/migrations/001_initial_schema.sql
	@echo "✅ Database migrations completed"

db-reset: ## Reset database
	@echo "🗄️ Resetting database..."
	docker-compose -f docker-compose.yml down postgres
	docker volume rm weather-forecaster_postgres_data
	docker-compose -f docker-compose.yml up -d postgres
	@echo "✅ Database reset completed"

# Production deployment
build-prod: ## Build production images
	@echo "🏭 Building production images..."
	docker-compose -f docker-compose.prod.yml build
	@echo "✅ Production images built"

deploy-prod: ## Deploy to production
	@echo "🚀 Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✅ Production deployment completed"

# Scaling
scale-kafka=%: ## Scale Kafka brokers (e.g., make scale-kafka=3)
	@echo "📡 Scaling Kafka to $(subst scale-kafka=,,$@) brokers..."
	docker-compose -f docker-compose.yml up -d --scale broker=$(subst scale-kafka=,,$@)
	@echo "✅ Kafka scaled to $(subst scale-kafka=,,$@) brokers"

scale-spark=%: ## Scale Spark workers (e.g., make scale-spark=2)
	@echo "⚡ Scaling Spark to $(subst scale-spark=,,$@) workers..."
	docker-compose -f docker-compose.yml up -d --scale spark-worker=$(subst scale-spark=,,$@)
	@echo "✅ Spark scaled to $(subst scale-spark=,,$@) workers"

# Utility commands
clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose -f docker-compose.yml down -v --remove-orphans
	docker system prune -f
	@echo "✅ Cleanup completed"

status: ## Show service status
	@echo "📊 Service Status:"
	docker-compose -f docker-compose.yml ps

dashboard: ## Open dashboard in browser
	@echo "🌐 Opening dashboard..."
	open http://localhost:8501 || xdg-open http://localhost:8501 || echo "Please open http://localhost:8501 in your browser"

monitor: ## Open monitoring in browser
	@echo "📈 Opening monitoring..."
	open http://localhost:3000 || xdg-open http://localhost:3000 || echo "Please open http://localhost:3000 in your browser"

api-docs: ## Generate API documentation
	@echo "📚 Generating API documentation..."
	docker-compose -f docker-compose.test.yml run --rm app python -m pydoc-markdown
	@echo "✅ API documentation generated"

# Health checks
health: ## Check service health
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8080/health || echo "❌ Airflow not healthy"
	@curl -f http://localhost:9021 || echo "❌ Kafka Control Center not healthy"
	@curl -f http://localhost:8501 || echo "❌ Dashboard not healthy"
	@echo "✅ Health check completed"

# Backup and restore
backup: ## Create database backup
	@echo "💾 Creating database backup..."
	docker-compose -f docker-compose.yml exec postgres pg_dump -U weatherflow weather_analytics > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created"

restore: ## Restore database from backup
	@echo "📥 Restoring database from backup..."
	@read -p "Enter backup file name: " backup_file; \
	docker-compose -f docker-compose.yml exec -T postgres psql -U weatherflow weather_analytics < $$backup_file
	@echo "✅ Database restored"

.PHONY: help install test test-cov lint format clean run docker-build docker-run

# Help
help:
	@echo "Supply Chain Optimizer - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install        - Install dependencies"
	@echo "  make install-test   - Install test dependencies"
	@echo "  make run            - Run the application locally"
	@echo "  make test           - Run all tests"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           - Run linting checks (flake8, pylint)"
	@echo "  make format         - Auto-format code (black, isort)"
	@echo "  make type-check     - Run type checking (mypy)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run application in Docker"
	@echo "  make docker-stop    - Stop Docker containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Remove temporary files and caches"

# Install
install:
	pip install -r requirements.txt

install-test:
	pip install -r requirements.txt -r requirements-test.txt

# Run
run:
	streamlit run frontend/app.py

run-dev:
	streamlit run frontend/app.py --logger.level=debug

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=backend --cov-report=html --cov-report=term-missing -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-fast:
	pytest tests/ -n auto -v

# Code Quality
lint:
	flake8 backend/ frontend/ tests/ --max-line-length=100
	pylint backend/ --disable=missing-docstring,too-few-public-methods

mypy:
	mypy backend/ --ignore-missing-imports

format:
	black backend/ frontend/ tests/
	isort backend/ frontend/ tests/

format-check:
	black --check backend/ frontend/ tests/
	isort --check-only backend/ frontend/ tests/

quality: format lint mypy

# Docker
docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/ build/ *.egg-info/
	@echo "Cleanup completed"

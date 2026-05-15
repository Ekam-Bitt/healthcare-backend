# ─────────────────────────────────────────────────────────────
# Healthcare Backend – Makefile
# ─────────────────────────────────────────────────────────────

.PHONY: help install run stop migrate makemigrations createsuperuser \
        test lint format clean docker-up docker-down shell flush

# Default target
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Setup ───────────────────────────────────────────────────

install: ## Install Python dependencies
	pip install -r requirements.txt

venv: ## Create virtual environment and install deps
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# ─── Development ─────────────────────────────────────────────

run: ## Start the development server
	python manage.py runserver 0.0.0.0:8000

stop: ## Stop the development server running on port 8000
	lsof -ti :8000 | xargs kill -9 2>/dev/null || echo "Server not running"

migrate: ## Apply database migrations
	python manage.py migrate

makemigrations: ## Create new migrations from model changes
	python manage.py makemigrations

createsuperuser: ## Create a Django admin superuser
	python manage.py createsuperuser

shell: ## Open Django interactive shell
	python manage.py shell

flush: ## Flush the database (⚠️  destructive)
	python manage.py flush --no-input

# ─── Testing ─────────────────────────────────────────────────

test: ## Run the test suite
	python manage.py test --verbosity=2

# ─── Code Quality ────────────────────────────────────────────

lint: ## Run flake8 linter
	flake8 accounts patients doctors mappings core

format: ## Auto-format code with black + isort
	isort accounts patients doctors mappings core
	black accounts patients doctors mappings core

check-format: ## Check formatting without modifying files
	black --check accounts patients doctors mappings core
	isort --check-only accounts patients doctors mappings core

# ─── Docker ──────────────────────────────────────────────────

docker-up: ## Start all services (PostgreSQL + Django) via Docker Compose
	docker compose up -d --build

docker-down: ## Stop all Docker Compose services
	docker compose down

docker-logs: ## Tail Docker Compose logs
	docker compose logs -f

# ─── Cleanup ─────────────────────────────────────────────────

clean: ## Remove compiled Python files and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true

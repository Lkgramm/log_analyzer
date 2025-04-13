# Переменные
PYTHON = poetry run python
POETRY = poetry
PYTEST = poetry run pytest
BLACK = poetry run black
ISORT = poetry run isort
FLAKE8 = poetry run flake8
MYPY = poetry run mypy
BANDIT = poetry run bandit

# Цели (targets)

## Установка зависимостей
install:
    $(POETRY) install

## Форматирование кода
format: clean-format
    $(BLACK) .
    $(ISORT) .

## Проверка форматирования
check-format:
    $(BLACK) --check .
    $(ISORT) --check-only .

## Линтинг кода
lint: check-format
    $(FLAKE8) .
    $(MYPY) log_analyzer/

## Тестирование
test:
    $(PYTEST) tests/ --cov=log_analyzer --cov-report=term-missing

## Безопасность: анализ кода на уязвимости
security:
    $(BANDIT) -r log_analyzer/ -ll

## Запуск скрипта
run:
    $(PYTHON) -m log_analyzer.main --config config.json

## Очистка временных файлов
clean:
    rm -rf .pytest_cache
    rm -rf __pycache__
    rm -rf .mypy_cache
    find . -type f -name "*.py[cod]" -delete

## Очистка отчетов и логов
clean-reports:
    rm -rf reports/*
    rm -rf logs/*

## Полная очистка
clean-all: clean clean-reports

## Помощь
help:
    @echo "Доступные команды:"
    @echo "  make install         - Установка зависимостей"
    @echo "  make format          - Форматирование кода (Black + isort)"
    @echo "  make lint            - Линтинг кода (Flake8 + MyPy)"
    @echo "  make test            - Запуск тестов с покрытием"
    @echo "  make security        - Анализ безопасности кода (Bandit)"
    @echo "  make run             - Запуск скрипта анализа логов"
    @echo "  make clean           - Очистка временных файлов"
    @echo "  make clean-reports   - Очистка директорий reports и logs"
    @echo "  make clean-all       - Полная очистка"
    @echo "  make help            - Показать эту справку"

.PHONY: install format check-format lint test security run clean clean-reports clean-all help
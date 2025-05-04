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
format:
	$(BLACK) .
	$(ISORT) .

## Линтинг кода
lint: check-format
	$(FLAKE8) log_analyzer/ tests/

## Тестирование
test:
	$(PYTEST) tests/ --cov=log_analyzer --cov-report=term-missing -v

## Безопасность: анализ кода на уязвимости
security:
	$(BANDIT) -r log_analyzer/ -ll

## Запуск скрипта
run:
	$(PYTHON) -m log_analyzer.main --config config.json

## Очистка временных файлов
clean:
	python -c "import shutil; import os; [shutil.rmtree(d) for d in ['.pytest_cache', '__pycache__', '.mypy_cache'] if os.path.exists(d)]"
	python -c "import os; [os.remove(f) for f in ['.coverage'] if os.path.exists(f)]"
	python -c "import glob; import os; [os.remove(f) for f in glob.glob('**/*.py[cod]', recursive=True)]"

## Очистка отчетов и логов
clean-reports:
	python -c "import shutil; import os; [shutil.rmtree(d) for d in ['reports'] if os.path.exists(d)]"

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
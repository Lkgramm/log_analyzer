# Log Analyzer

Log Analyzer — это инструмент для анализа логов веб-сервера Nginx. Он собирает статистику по URL'ам (количество запросов, суммарное время обработки, медиана и т.д.) и генерирует HTML-отчет с таблицей, отсортированной по времени обработки.

---

## Содержание

1. [Описание](#описание)
2. [Формат логов](#формат-логов)
3. [Требования](#требования)
4. [Установка](#установка)
5. [Использование](#использование)
6. [Конфигурация](#конфигурация)
7. [Тестирование](#тестирование)
8. [Разработка](#разработка)
9. [Контейнеризация](#контейнеризация)
10. [Лицензия](#лицензия)

---

## Описание

Log Analyzer анализирует логи Nginx, собирает статистику по URL'ам и генерирует HTML-отчет. Отчет содержит следующие метрики:
- `count`: Количество запросов.
- `count_perc`: Процент от общего числа запросов.
- `time_sum`: Суммарное время обработки.
- `time_perc`: Процент от общего времени обработки.
- `time_avg`: Среднее время обработки.
- `time_max`: Максимальное время обработки.
- `time_med`: Медиана времени обработки.

Отчет сохраняется в формате HTML и поддерживает сортировку таблицы.

---

## Формат логов

Логи должны соответствовать формату `ui_short` Nginx:

```
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '  
                     '$request_time';
```

Пример строки лога:
```
1.196.116.32 - - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390
```

Ключевые поля:
- `$remote_addr`: IP-адрес клиента.
- `$remote_user`: Пользователь (чаще всего `-`).
- `$http_x_real_ip`: Реальный IP-адрес (может быть `-`).
- `[$time_local]`: Время запроса.
- `"$request"`: HTTP-запрос (например, `"GET /api/v2/banner/25019354 HTTP/1.1"`).
- `$status`: Код ответа сервера.
- `$body_bytes_sent`: Размер ответа в байтах.
- `"$http_referer"`: Реферер.
- `"$http_user_agent"`: User-Agent.
- `"$http_x_forwarded_for"`: X-Forwarded-For.
- `"$http_X_REQUEST_ID"`: Идентификатор запроса.
- `"$http_X_RB_USER"`: Идентификатор пользователя.
- `$request_time`: Время обработки запроса (в секундах).

---

## Требования

- Python 3.8+
- Poetry (для управления зависимостями)
- Docker (опционально, для контейнеризации)

---

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your-repo/log-analyzer.git
   cd log-analyzer
   ```

2. **Установите зависимости:**
   ```bash
   poetry install
   ```

3. **Создайте директории для логов и отчетов:**
   ```bash
   mkdir logs reports
   ```

4. **(Опционально) Настройте pre-commit хуки:**
   ```bash
   poetry run pre-commit install
   ```

---

## Использование

### Запуск скрипта

```bash
poetry run python -m log_analyzer.main --config path/to/config.json
```

Если путь к конфигу не указан, используется дефолтный конфиг.

### Пример команды

```bash
poetry run python -m log_analyzer.main --config config.json
```

---

## Конфигурация

Файл конфигурации (`config.json`) содержит следующие параметры:

```json
{
  "REPORT_SIZE": 1000,          // Количество URL'ов в отчете
  "REPORT_DIR": "./reports",    // Директория для сохранения отчетов
  "LOG_DIR": "./logs",          // Директория с логами
  "LOG_FILE": "./log_analyzer.log", // Файл для логирования (или null для stdout)
  "ERROR_THRESHOLD": 0.3        // Порог ошибок парсинга (в долях)
}
```

Если файл конфигурации не существует или не парсится, скрипт завершается с ошибкой.

---

## Тестирование

### Запуск тестов

```bash
make test
```

Или через Poetry:
```bash
poetry run pytest tests/
```

### Проверка кода

Запустите линтеры и форматтеры:
```bash
make lint
```

---

## Разработка

### Структура проекта

```
log_analyzer/
├── log_analyzer/               # Основной пакет
│   ├── main.py                 # Точка входа
│   ├── config.py               # Работа с конфигурацией
│   ├── log_parser.py           # Парсер логов
│   ├── report_generator.py     # Генерация отчета
│   └── utils.py                # Вспомогательные функции
├── templates/                  # Шаблоны HTML
├── static/                     # Статические файлы
├── tests/                      # Тесты
├── .pre-commit-config.yaml     # Pre-commit хуки
├── pyproject.toml              # Настройки Poetry
├── Makefile                    # Удобные команды
└── Dockerfile                  # Dockerfile
```

### Команды для разработки

- **Запуск линтеров:**
  ```bash
  make lint
  ```

- **Запуск тестов:**
  ```bash
  make test
  ```

- **Запуск скрипта:**
  ```bash
  make run
  ```

---

## Контейнеризация

### Сборка Docker-образа

```bash
docker build -t log-analyzer .
```

### Запуск контейнера

```bash
docker run -v /path/to/logs:/logs -v /path/to/reports:/reports log-analyzer
```

- `/path/to/logs`: Директория с логами на вашем компьютере.
- `/path/to/reports`: Директория для сохранения отчетов.

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

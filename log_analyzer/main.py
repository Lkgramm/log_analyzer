import logging
from pathlib import Path

from log_analyzer.config import load_config
from log_analyzer.log_parser import find_latest_log, parse_log
from log_analyzer.report_generator import (
    collect_statistics,
    generate_report,
    is_report_exists,
)
from log_analyzer.utils import setup_logging


def main():
    # Загрузка конфигурации
    config = load_config("config.json")

    # Настройка логирования
    setup_logging(level=logging.INFO)
    logging.info("Starting log analyzer...")

    # Поиск последнего лога
    try:
        latest_log = find_latest_log(config["LOG_DIR"])
        logging.info(f"Latest log file found: {latest_log.path}")
    except FileNotFoundError as e:
        logging.error(e)
        return

    # Проверка отчета к последнему логу
    if is_report_exists(config["REPORT_DIR"], latest_log.date.strftime("%Y.%m.%d")):
        logging.info("Report already exists, skipping processing")
        return

    # Парсинг логов
    parsed_logs = list(parse_log(latest_log))

    # Сбор статистики
    stats, total_count, total_time, parsing_errors = collect_statistics(parsed_logs)

    # Генерация отчета
    report_date = latest_log.date.strftime("%Y.%m.%d")
    report_path = Path(config["REPORT_DIR"])
    generate_report(stats, report_date, report_path, config["REPORT_SIZE"])


if __name__ == "__main__":
    main()

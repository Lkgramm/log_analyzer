import logging
import sys
from pathlib import Path


def setup_logging(log_file=None, level=logging.INFO):
    """
    Настройка системы логирования.
    :param log_file: Путь к файлу логов (если None, логи выводятся в stdout).
    :param level: Уровень логирования.
    """
    handlers = []
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Логирование в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # Логирование в файл (если указан)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(
            parents=True, exist_ok=True
        )  # Создаем директорию, если её нет
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logging.basicConfig(level=level, handlers=handlers)

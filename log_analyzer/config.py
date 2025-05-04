import json
from pathlib import Path

DEFAULT_CONFIG = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./logs"}


def load_config(config_path=None):
    """
    Загружает и объединяет конфигурацию из файла с дефолтным конфигом.
    Если файл конфигурации не найден или пуст, используется только дефолтный конфиг.
    """
    config = DEFAULT_CONFIG.copy()  # Копируем дефолтный конфиг

    if config_path:
        config_file = Path(config_path)
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    file_config = json.load(f)
                # Объединяем дефолтный конфиг и конфиг из файла
                config.update(file_config)
            except json.JSONDecodeError:
                print(
                    f"Warning: Invalid JSON in config file: {config_path}. Using default config."
                )
        else:
            print(
                f"Warning: Config file not found: {config_path}. Using default config."
            )

    return config

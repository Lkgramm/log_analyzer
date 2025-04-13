import json

DEFAULT_CONFIG = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./logs"
}

def load_config(config_path):
    """
    Загружает и объединяет конфигурацию из файла с дефолтным конфигом.
    """
    try:
        with open(config_path, "r") as f:
            file_config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in config file: {config_path}")

    # Объединяем дефолтный конфиг и конфиг из файла
    config = {**DEFAULT_CONFIG, **file_config}
    return config
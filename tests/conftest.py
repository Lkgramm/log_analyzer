import os
import tempfile

import pytest


@pytest.fixture
def temp_log_file():
    """Создает временный файл логов."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(
            '1.2.3.4 - - [29/Jun/2023:12:00:00 +0300] "GET /api/test HTTP/1.1" 200 123 "-" "-" "-" "-" 0.123\n'
        )
        f.write(
            '1.2.3.5 - - [29/Jun/2023:12:00:01 +0300] "POST /api/test2 HTTP/1.1" 200 456 "-" "-" "-" "-" 0.456\n'
        )
    yield f.name
    os.unlink(f.name)


@pytest.fixture
def temp_config_file():
    """Создает временный конфигурационный файл."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(
            '{"REPORT_SIZE": 10, "REPORT_DIR": "./reports", "LOG_DIR": "./logs", "ERROR_THRESHOLD": 0.3}'
        )
    yield f.name
    os.unlink(f.name)

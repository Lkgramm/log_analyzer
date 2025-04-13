from log_analyzer.log_parser import parse_log
from collections import namedtuple

LogFile = namedtuple("LogFile", ["path", "date", "extension"])

def test_parse_log(temp_log_file):
    """Тестирование парсинга строк логов."""
    log_file = LogFile(path=temp_log_file, date=None, extension="plain")
    parsed_logs = list(parse_log(log_file))

    # Проверка количества распарсенных строк
    assert len(parsed_logs) == 2

    # Проверка содержимого первой строки
    url, request_time = parsed_logs[0]
    assert url == "/api/test"
    assert request_time == 0.123

    # Проверка содержимого второй строки
    url, request_time = parsed_logs[1]
    assert url == "/api/test2"
    assert request_time == 0.456
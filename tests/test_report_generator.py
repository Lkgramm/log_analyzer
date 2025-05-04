import os
from collections import defaultdict

from log_analyzer.report_generator import collect_statistics, generate_report


def test_collect_statistics():
    """Тестирование сбора статистики."""
    parsed_logs = [
        ("/api/test", 0.123),
        ("/api/test2", 0.456),
        ("/api/test", 0.789),
    ]
    stats, total_count, total_time, parsing_errors = collect_statistics(parsed_logs)

    # Проверка общего количества запросов
    assert total_count == 3

    # Проверка общей суммы времени
    assert round(total_time, 3) == 1.368

    # Проверка статистики для первого URL
    data = stats["/api/test"]
    assert data["count"] == 2
    assert round(data["time_sum"], 3) == 0.912
    assert round(data["time_avg"], 3) == 0.456
    assert round(data["time_max"], 3) == 0.789
    assert round(data["time_med"], 3) == 0.456


def test_generate_report(tmpdir):
    """Тестирование генерации отчета."""
    stats = {
        "/api/test": {
            "count": 2,
            "count_perc": 66.667,
            "time_sum": 0.912,
            "time_perc": 66.667,
            "time_avg": 0.456,
            "time_max": 0.789,
            "time_med": 0.456,
        },
        "/api/test2": {
            "count": 1,
            "count_perc": 33.333,
            "time_sum": 0.456,
            "time_perc": 33.333,
            "time_avg": 0.456,
            "time_max": 0.456,
            "time_med": 0.456,
        },
    }
    report_date = "2023.06.29"
    report_dir = str(tmpdir.mkdir("reports"))
    generate_report(stats, report_date, report_dir, report_size=10)

    # Проверка, что отчет был создан
    report_path = os.path.join(report_dir, f"report-{report_date}.html")
    assert os.path.exists(report_path)

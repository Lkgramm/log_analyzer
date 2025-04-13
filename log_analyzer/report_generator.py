import json
import structlog
import os
from statistics import median
from collections import defaultdict
from string import Template
from typing import Generator, Tuple


def collect_statistics(parsed_log: Generator[Tuple[str, float], None, None]) -> dict:
    stats = defaultdict(lambda: {"count": 0, "time_sum": 0, "time_max": 0, "time_list": []})
    total_count = 0
    total_time = 0
    parsing_errors = 0

    for url, request_time in parsed_log:
        if url is None or request_time is None:
            parsing_errors += 1
            continue

        total_count += 1
        total_time += request_time
        stats[url]["count"] += 1
        stats[url]["time_sum"] += request_time
        stats[url]["time_max"] = max(stats[url]["time_max"], request_time)
        stats[url]["time_list"].append(request_time)

    # Логируем общее количество ошибок парсинга
    structlog.get_logger().info(
        "Parsing statistics",
        total_lines=total_count + parsing_errors,
        parsed_lines=total_count,
        parsing_errors=parsing_errors,
    )

    # Вычисляем дополнительные метрики
    for url, data in stats.items():
        data["count_perc"] = (data["count"] / total_count) * 100
        data["time_perc"] = (data["time_sum"] / total_time) * 100
        data["time_avg"] = data["time_sum"] / data["count"]
        data["time_med"] = median(data["time_list"])

    return stats, total_count, total_time, parsing_errors

def generate_report(stats: dict, report_date: str, report_dir: str, report_size: int) -> None:
    # Сортируем URL'ы по time_sum
    sorted_urls = sorted(stats.items(), key=lambda x: x[1]["time_sum"], reverse=True)[:report_size]

    # Формируем данные для таблицы
    table_json = [
        {
            "url": url,
            "count": data["count"],
            "count_perc": round(data["count_perc"], 3),
            "time_sum": round(data["time_sum"], 3),
            "time_perc": round(data["time_perc"], 3),
            "time_avg": round(data["time_avg"], 3),
            "time_max": round(data["time_max"], 3),
            "time_med": round(data["time_med"], 3),
        }
        for url, data in sorted_urls
    ]

    # Читаем шаблон
    with open("templates/report.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Подставляем данные в $table_json
    report_content = template.safe_substitute(table_json=json.dumps(table_json))

    # Сохраняем отчет
    report_path = os.path.join(report_dir, f"report-{report_date}.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
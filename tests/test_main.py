import json
from log_analyzer.main import main
from log_analyzer.config import load_config

def test_main_with_log_file(tmpdir):
    # Создание временного конфига
    config_path = tmpdir / "config.json"
    config = {
        "REPORT_SIZE": 10,
        "REPORT_DIR": str(tmpdir),
        "LOG_DIR": str(tmpdir)
    }
    with open(config_path, "w") as f:
        json.dump(config, f)

    # Создание временного лог-файла
    log_file = tmpdir / "nginx-access-ui.log-20231001.gz"
    with open(log_file, "wb") as f:
        f.write(b"Test log data")

    # Запуск основной функции
    main()

    # Проверка, что отчет был создан
    report_files = [f for f in tmpdir.listdir() if f.basename.startswith("report-")]
    assert len(report_files) > 0, "No report files were generated"
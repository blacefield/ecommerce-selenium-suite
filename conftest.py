import os
import glob
import logging
import pytest
from datetime import datetime

def pytest_configure(config):
    # Project and log folder setup
    project_root = os.path.dirname(__file__)
    log_folder = os.path.join(project_root, "logs")
    os.makedirs(log_folder, exist_ok=True)

    # Determine test name for log file naming
    test_paths = config.args
    if test_paths:
        test_name_raw = os.path.splitext(os.path.basename(test_paths[0]))[0]
    else:
        test_name_raw = "full_suite"
    test_name_upper = test_name_raw.upper()

    # Timestamped log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    log_file_name = f"{test_name_raw}_{timestamp}.txt"
    log_file_path = os.path.join(log_folder, log_file_name)

    # Keep only 5 most recent logs for this test type
    matching_logs = glob.glob(os.path.join(log_folder, f"{test_name_raw}_*.txt"))
    matching_logs.sort(key=os.path.getmtime)
    if len(matching_logs) >= 5:
        for file in matching_logs[:len(matching_logs) - 4]:
            os.remove(file)

    # Clear existing handlers to avoid duplicate logs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Manually write the header
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("\n\n")
        f.write(f"{test_name_upper} TEST\n")
        f.write("\n")

    # Set up logging to file, appending below the header
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Attach to logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logging.info("Logging initialized with full output.")
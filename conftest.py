import os
import glob
import logging
import pytest
import time
from datetime import datetime
from utils.html_reporter import HTMLReportGenerator

# Global variables for session tracking
_logging_initialized = False
_html_reporter = None
_session_start_time = None
_test_start_times = {}

def pytest_configure(config):
    """Called once at the start of the entire pytest session"""
    global _logging_initialized, _html_reporter, _session_start_time
    
    # Only initialize once per session
    if _logging_initialized:
        return
    
    _session_start_time = datetime.now()
    
    # Initialize HTML reporter
    _html_reporter = HTMLReportGenerator("Selenium E2E Test Suite")
    
    # Setup directories
    project_root = os.path.dirname(__file__)
    log_folder = os.path.join(project_root, "logs")
    reports_folder = os.path.join(project_root, "reports")
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(reports_folder, exist_ok=True)

    # Determine test name for file naming
    test_paths = config.args
    if test_paths:
        test_name_raw = os.path.splitext(os.path.basename(test_paths[0]))[0]
    else:
        test_name_raw = "full_suite"
    
    test_name_upper = test_name_raw.upper()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Setup log file
    log_file_name = f"{test_name_raw}_{timestamp}.txt"
    log_file_path = os.path.join(log_folder, log_file_name)

    # Keep only 5 most recent logs for this test type
    matching_logs = glob.glob(os.path.join(log_folder, f"{test_name_raw}_*.txt"))
    matching_logs.sort(key=os.path.getmtime)
    if len(matching_logs) >= 5:
        for file in matching_logs[:len(matching_logs) - 4]:
            try:
                os.remove(file)
            except OSError:
                pass

    # Clear existing log handlers
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Write log header
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(f"\n{test_name_upper} TEST SESSION\n")
        f.write(f"Started: {_session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

    # Setup file logging
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    # Store HTML report path
    report_file_name = f"{test_name_raw}_report_{timestamp}.html"
    config._html_report_path = os.path.join(reports_folder, report_file_name)
    
    _logging_initialized = True
    logging.info("Logging and HTML reporting initialized.")

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    logging.info(f"Test session started with {len(session.config.args)} test file(s)")

def pytest_runtest_setup(item):
    """Called before each test runs"""
    global _test_start_times
    test_name = item.name
    _test_start_times[test_name] = time.time()
    logging.info(f"🚀 Starting: {test_name}")

def pytest_runtest_teardown(item, nextitem):
    """Called after each test completes"""
    test_name = item.name
    logging.info(f"🏁 Finished: {test_name}")

def pytest_runtest_logreport(report):
    """Called when a test report is created"""
    global _html_reporter, _test_start_times
    
    if report.when == "call":  # Only process main test execution
        test_name = report.nodeid.split("::")[-1]
        
        # Calculate test duration
        duration = 0
        if test_name in _test_start_times:
            duration = time.time() - _test_start_times[test_name]
            del _test_start_times[test_name]
        
        # Determine status and collect details
        status = "PASSED"
        error_message = ""
        details = f"Test: {test_name}\nDuration: {duration:.2f}s"
        
        if report.failed:
            status = "FAILED"
            if report.longrepr:
                error_message = str(report.longrepr)
                # Get concise error info
                lines = error_message.split('\n')
                for line in lines:
                    line = line.strip()
                    if ('assert' in line.lower() or 'error:' in line.lower()) and line:
                        details += f"\nError: {line}"
                        break
            logging.error(f"❌ FAILED: {test_name}")
        elif report.skipped:
            status = "SKIPPED"
            if hasattr(report, 'wasxfail'):
                details += f"\nReason: {report.wasxfail}"
            logging.warning(f"⚠️  SKIPPED: {test_name}")
        else:
            logging.info(f"✅ PASSED: {test_name}")
        
        # Add to HTML reporter
        if _html_reporter:
            _html_reporter.add_test_result(
                test_name=test_name,
                status=status,
                duration=duration,
                details=details,
                error_message=error_message[:1000] if error_message else ""  # Limit error length
            )

def pytest_sessionfinish(session, exitstatus):
    """Called after the entire test session finishes"""
    global _html_reporter, _session_start_time
    
    session_end_time = datetime.now()
    total_duration = (session_end_time - _session_start_time).total_seconds()
    
    total_tests = session.testscollected
    failed_count = session.testsfailed
    passed_count = total_tests - failed_count
    
    # Log session summary
    logging.info("=" * 60)
    logging.info("TEST SESSION SUMMARY")
    logging.info("=" * 60)
    logging.info(f"Total Tests: {total_tests}")
    logging.info(f"Passed: {passed_count}")
    logging.info(f"Failed: {failed_count}")
    logging.info(f"Duration: {total_duration:.2f}s")
    logging.info(f"Exit Status: {exitstatus}")
    logging.info(f"Session finished: {session_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Generate HTML report
    if _html_reporter and hasattr(session.config, '_html_report_path'):
        try:
            _html_reporter.set_session_times(_session_start_time, session_end_time)
            report_path = _html_reporter.generate_html_report(session.config._html_report_path)
            
            abs_report_path = os.path.abspath(report_path)
            logging.info(f"📊 HTML Report: {abs_report_path}")
            
            # Print to console so user can see it
            print(f"\n📊 HTML Report Generated!")
            print(f"📁 File: {abs_report_path}")
            print(f"🌐 Browser: file://{abs_report_path}")
            print(f"📈 Summary: {passed_count}/{total_tests} tests passed ({(passed_count/total_tests*100 if total_tests > 0 else 0):.1f}%)")
            
        except Exception as e:
            logging.error(f"❌ Failed to generate HTML report: {str(e)}")
            print(f"❌ HTML report generation failed: {str(e)}")
    
    logging.info("=" * 60)
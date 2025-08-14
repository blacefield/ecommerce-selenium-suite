import json
import os
from datetime import datetime
from typing import Dict, List, Any

class HTMLReportGenerator:
    """Generate beautiful HTML reports from test results"""
    
    def __init__(self, project_name="QA Automation Test Suite"):
        self.project_name = project_name
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
    def add_test_result(self, test_name: str, status: str, duration: float = 0, 
                       details: str = "", error_message: str = "", screenshot_path: str = "", 
                       browser: str = ""):
        """Add a test result to the report"""
        self.test_results.append({
            'name': test_name,
            'status': status.upper(),
            'duration': duration,
            'details': details,
            'error_message': error_message,
            'screenshot_path': screenshot_path,
            'timestamp': datetime.now().isoformat(),
            'browser': browser.lower() if browser else ""
        })
    
    def set_session_times(self, start_time: datetime, end_time: datetime):
        """Set the session start and end times"""
        self.start_time = start_time
        self.end_time = end_time
    
    def generate_html_report(self, output_path: str) -> str:
        """Generate the HTML report"""
        # Ensure reports directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASSED')
        failed_tests = sum(1 for result in self.test_results if result['status'] == 'FAILED')
        skipped_tests = sum(1 for result in self.test_results if result['status'] == 'SKIPPED')
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        total_duration = sum(result['duration'] for result in self.test_results)
        
        # Generate HTML content
        html_content = self._generate_html_template(
            total_tests, passed_tests, failed_tests, skipped_tests, 
            pass_rate, total_duration
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_html_template(self, total_tests: int, passed_tests: int, 
                               failed_tests: int, skipped_tests: int, 
                               pass_rate: float, total_duration: float) -> str:
        """Generate the complete HTML template"""
        
         # Calculate browser statistics
        browser_stats = self._get_browser_statistics()
        browser_summary_cards = self._generate_browser_summary_cards(browser_stats)
        
        # Test results table rows
        test_rows = ""
        for i, result in enumerate(self.test_results, 1):
            status_class = result['status'].lower()
            status_icon = self._get_status_icon(result['status'])
            duration_str = f"{result['duration']:.2f}s" if result['duration'] > 0 else "N/A"
            
             # Add browser icon to the display name
            browser = result.get('browser', 'unknown')
            browser_icon = self._get_browser_icon(browser)
            display_name = result['name']

            error_details = ""
            if result['error_message']:
                error_details = f"""
                <div class="error-details" style="display: none;">
                    <pre>{result['error_message']}</pre>
                </div>
                """
            
            test_rows += f"""
            <tr class="test-row {status_class}" data-browser="{browser}"onclick="toggleDetails({i})">
                <td>{i}</td>
                <td class="test-name">
                    <span class="browser-icon">{browser_icon}</span>
                    {display_name}
                </td>
                <td class="status {status_class}">
                    <span class="status-icon">{status_icon}</span>
                    {result['status']}
                </td>
                <td>{duration_str}</td>
                <td>{result.get('timestamp', '').split('T')[1][:8] if result.get('timestamp') else 'N/A'}</td>
            </tr>
            <tr class="details-row" id="details-{i}" data-browser="{browser}"style="display: none;">
                <td colspan="5">
                    <div class="test-details">
                        {result['details']}
                        {error_details}
                    </div>
                </td>
            </tr>
            """
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.project_name} - Cross-Browser Test Report</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{self.project_name}</h1>
            <h2>Cross-Browser Test Execution Report</h2>
            <div class="report-meta">
                <span>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                <span>Duration: {total_duration:.2f}s</span>
                <span>Browsers: {len(browser_stats)} tested</span>
            </div>
        </header>

        <div class="summary-cards">
            <div class="card total">
                <h3>Total Tests</h3>
                <div class="number">{total_tests}</div>
            </div>
            <div class="card passed">
                <h3>Passed</h3>
                <div class="number">{passed_tests}</div>
            </div>
            <div class="card failed">
                <h3>Failed</h3>
                <div class="number">{failed_tests}</div>
            </div>
            <div class="card skipped">
                <h3>Skipped</h3>
                <div class="number">{skipped_tests}</div>
            </div>
            <div class="card pass-rate">
                <h3>Pass Rate</h3>
                <div class="number">{pass_rate:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_rate}%"></div>
                </div>
            </div>
        </div>

        {browser_summary_cards}

        <div class="test-results">
            <h3>Test Results by Browser</h3>
             <div class="browser-filter">
                <button class="filter-btn active" onclick="filterByBrowser('all')">All Browsers</button>
                <button class="filter-btn" onclick="filterByBrowser('chrome')">🟡 Chrome</button>
                <button class="filter-btn" onclick="filterByBrowser('firefox')">🟠 Firefox</button>
                <button class="filter-btn" onclick="filterByBrowser('edge')">🔵 Edge</button>
            </div>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody id="test-results-body">
                    {test_rows}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
    
    def _get_browser_statistics(self):
        """Calculate statistics per browser"""
        browser_stats = {}
        for result in self.test_results:
            browser = result.get('browser', 'unknown')
            if browser not in browser_stats:
                browser_stats[browser] = {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0}
            
            browser_stats[browser]['total'] += 1
            if result['status'] == 'PASSED':
                browser_stats[browser]['passed'] += 1
            elif result['status'] == 'FAILED':
                browser_stats[browser]['failed'] += 1
            elif result['status'] == 'SKIPPED':
                browser_stats[browser]['skipped'] += 1
        
        return browser_stats
    
    def _generate_browser_summary_cards(self, browser_stats):
        """Generate browser-specific summary cards"""
        if not browser_stats:
            return ""
        
        cards_html = '<div class="browser-summary-cards"><h3>Browser Performance</h3><div class="browser-cards">'
        
        for browser, stats in browser_stats.items():
            if browser == 'unknown':
                continue
                
            browser_icon = self._get_browser_icon(browser)
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            cards_html += f"""
            <div class="browser-card">
                <div class="browser-header">
                    <span class="browser-icon-large">{browser_icon}</span>
                    <h4>{browser.title()}</h4>
                </div>
                <div class="browser-stats">
                    <div class="stat">
                        <span class="stat-number">{stats['total']}</span>
                        <span class="stat-label">Total</span>
                    </div>
                    <div class="stat passed">
                        <span class="stat-number">{stats['passed']}</span>
                        <span class="stat-label">Passed</span>
                    </div>
                    <div class="stat failed">
                        <span class="stat-number">{stats['failed']}</span>
                        <span class="stat-label">Failed</span>
                    </div>
                </div>
                <div class="browser-pass-rate">
                    <span>{pass_rate:.1f}% Pass Rate</span>
                    <div class="mini-progress-bar">
                        <div class="mini-progress-fill" style="width: {pass_rate}%"></div>
                    </div>
                </div>
            </div>
            """
        
        cards_html += '</div></div>'
        return cards_html
    
    def _get_browser_icon(self, browser):
        """Get emoji icon for browser"""
        icons = {
            'chrome': '🟡',
            'firefox': '🟠', 
            'edge': '🔵'
        }
        return icons.get(browser.lower(), '🌐')

    def _get_status_icon(self, status: str) -> str:
        """Get icon for test status"""
        icons = {
            'PASSED': '✅',
            'FAILED': '❌', 
            'SKIPPED': '⚠️',
            'ERROR': '💥'
        }
        return icons.get(status, '❓')
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for the HTML report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header h2 {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .report-meta {
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
        }
        
        .card h3 {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .card .number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .card.total .number { color: #3498db; }
        .card.passed .number { color: #27ae60; }
        .card.failed .number { color: #e74c3c; }
        .card.skipped .number { color: #f39c12; }
        .card.pass-rate .number { color: #9b59b6; }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            transition: width 0.3s ease;
        }
        
        .test-results {
            padding: 30px;
        }
        
        .test-results h3 {
            margin-bottom: 20px;
            color: #2c3e50;
            font-size: 1.5em;
        }
        
        .results-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .results-table th {
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .results-table td {
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .test-row {
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .test-row:hover {
            background: #f8f9fa;
        }
        
        .test-row.passed {
            border-left: 4px solid #27ae60;
        }
        
        .test-row.failed {
            border-left: 4px solid #e74c3c;
        }
        
        .test-row.skipped {
            border-left: 4px solid #f39c12;
        }
        
        .status {
            font-weight: bold;
        }
        
        .status.passed { color: #27ae60; }
        .status.failed { color: #e74c3c; }
        .status.skipped { color: #f39c12; }
        
        .status-icon {
            margin-right: 8px;
        }
        
        .test-name {
            font-weight: 500;
        }
        
        .details-row {
            background: #f8f9fa;
        }
        
        .test-details {
            padding: 20px;
            background: white;
            border-radius: 4px;
            margin: 10px 0;
        }
        
        .error-details pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        @media (max-width: 768px) {
            .summary-cards {
                grid-template-columns: 1fr 1fr;
            }
            
            .results-table {
                font-size: 0.9em;
            }
            
            .results-table th,
            .results-table td {
                padding: 10px 8px;
            }
        }
        .browser-summary-cards {
            padding: 0 30px;
            background: #f8f9fa;
        }
        
        .browser-summary-cards h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        .browser-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .browser-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .browser-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .browser-icon-large {
            font-size: 2em;
            margin-right: 10px;
        }
        
        .browser-header h4 {
            color: #2c3e50;
            font-size: 1.2em;
        }
        
        .browser-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            display: block;
            font-size: 1.5em;
            font-weight: bold;
            color: #3498db;
        }
        
        .stat.passed .stat-number { color: #27ae60; }
        .stat.failed .stat-number { color: #e74c3c; }
        
        .stat-label {
            font-size: 0.8em;
            color: #666;
            text-transform: uppercase;
        }
        
        .browser-pass-rate {
            text-align: center;
            font-size: 0.9em;
            color: #666;
        }
        
        .mini-progress-bar {
            width: 100%;
            height: 4px;
            background: #ecf0f1;
            border-radius: 2px;
            margin-top: 5px;
        }
        
        .mini-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            border-radius: 2px;
        }
        
        .browser-filter {
            margin-bottom: 20px;
            text-align: center;
        }
        
        .filter-btn {
            background: #ecf0f1;
            border: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .filter-btn:hover {
            background: #bdc3c7;
        }
        
        .filter-btn.active {
            background: #3498db;
            color: white;
        }
        
        .browser-icon {
            margin-right: 8px;
            font-size: 1.1em;
        }
        
        .test-row[data-browser="chrome"] { border-left-color: #FFC107; }
        .test-row[data-browser="firefox"] { border-left-color: #FF9800; }
        .test-row[data-browser="edge"] { border-left-color: #2196F3; }
        """
    
    def _get_javascript(self) -> str:
        """Get JavaScript for the HTML report"""
        return """
        function toggleDetails(rowNum) {
            const detailsRow = document.getElementById('details-' + rowNum);
            if (detailsRow.style.display === 'none') {
                detailsRow.style.display = 'table-row';
            } else {
                detailsRow.style.display = 'none';
            }
        }

        function filterByBrowser(browser) {
            console.log('Filtering by browser:', browser);
            
            const allRows = document.querySelectorAll('#test-results-body tr');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Filter rows based on data-browser attribute
            allRows.forEach(row => {
                const rowBrowser = row.getAttribute('data-browser');
                
                if (browser === 'all' || rowBrowser === browser) {
                    row.style.display = 'table-row';
                } else {
                    row.style.display = 'none';
                }
                
                // Always hide details rows when filtering
                if (row.classList.contains('details-row')) {
                    row.style.display = 'none';
                }
            });
        }

        // Add smooth scrolling
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.card');
            cards.forEach(card => {
                card.addEventListener('click', function() {
                    document.querySelector('.test-results').scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        });
        """

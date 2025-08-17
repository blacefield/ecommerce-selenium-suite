# E-Commerce Selenium Automation Suite

## Overview
This project was created as part of my QA Automation Engineer portfolio to demonstrate **code-first Selenium testing practices** using Python and pytest.  
It simulates real-world end-to-end (E2E) testing scenarios for a sample e-commerce web application, including login, product browsing, adding items to the cart, and completing checkout.  

While my earlier automation experience includes low-code tools like Telerik and TestComplete, this project bridges the gap to **fully code-driven frameworks**, showcasing:
- Scalable and maintainable **Page Object Model (POM)** architecture
- **Data-driven testing** with external JSON datasets
- Structured logging and **HTML reporting**
- Readiness for integration with CI/CD pipelines

---

## Goals
- Simulate realistic E2E testing workflows
- Demonstrate maintainable, modular automation design
- Showcase data-driven tests, reusable page objects, and structured logs
- Provide HTML-based execution reports for visibility and traceability

---

## Project Structure
ecommerce-selenium-suite/
 README.txt → Project documentation
 requirements.txt → Python dependencies
 conftest.py → Pytest fixtures for setup/teardown

 ─ data/ → JSON test datasets
 ─ logs/ → Text execution logs (plain txt files)
 ─ pages/ → Page Object Model classes
 ─ reports/ → HTML test reports (professional, visual results)
 ─ tests/ → Test cases organized by functionality
 ─ utils/ → Helper functions

---

## Technologies Used
- **Python 3.x**
- **Selenium WebDriver**
- **pytest** (test runner)
- **pytest-html** (HTML reporting)
- **JSON** for test data management

---

## Test Coverage
Currently implemented:
- **Login** (basic & data-driven)
- **Inventory browsing**
- **Add to cart**
- **End-to-end checkout**

Planned:
- More negative scenarios (invalid credentials, locked accounts, expired cart, etc)
- Edge cases (empty cart checkout, out-of-stock handling)
- API-level validation for certain flows

---

## How to Set Up and Run

### Prerequisites
- **Python 3.x** installed on your system
- **Chrome Browser** installed
- **ChromeDriver** matching your Chrome version (place it in your PATH)

### Installation
1. Clone the repository:
    git clone https://github.com/blacefield/ecommerce-selenium-suite.git
    cd ecommerce-selenium-suite

2. Install dependencies:
    pip install -r requirements.txt

### Running Tests
- Run a specific test file:
    pytest tests/login.py -v
- Run all tests:
    pytest tests/ -v

---

## Reporting
This project uses **pytest-html** for HTML-based test execution reports.

- Reports are generated in the `reports/` folder.
- Each test run produces a timestamped `.html` file.
- Reports include:
  - Pass/fail summary
  - Detailed step logs
  - Screenshots on failure (if configured)

Example:

reports/
    add_to_cart_report_2025-08-14_1320.html
    e2e_checkout_report_2025-08-14_1310.html

---

## Logging
- Raw `.txt` execution logs are saved in the `logs/` directory for traceability.
- Each log file contains timestamped actions and assertions.

---

## Future Improvements
To make this project even more production-ready:
1. **CI/CD Integration**
    Add GitHub Actions/Jenkins pipeline to run tests automatically on push and pull requests.
    Store HTML reports as build artifacts.
2. **Config Management**
    Move URLs, credentials, and browser settings into a `config.json` or `.env` file.
3. **Negative and Edge Case Coverage**
    Include more scenarios beyond happy paths.


---

## Author
Brandon Lacefield  
QA Automation Engineer  
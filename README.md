# E-Commerce Selenium Automation Suite

[![E2E Tests](https://github.com/blacefield/ecommerce-selenium-suite/actions/workflows/e2e-tests.yml/badge.svg?branch=master)](https://github.com/blacefield/ecommerce-selenium-suite/actions/workflows/e2e-tests.yml)

## Overview
This project demonstrates **code-first Selenium test automation** using Python and pytest.  
It simulates real-world e-commerce user journeys: login, product browsing, adding items to the cart, and checkout.

It showcases:
- **Page Object Model (POM)** for scalability
- **Data-driven testing** with JSON
- **Structured logging and HTML reports**
- **Continuous Integration with GitHub Actions**

---

## Why This Project Matters
As part of my QA Automation portfolio, this project highlights my ability to:
- Build maintainable automation frameworks from scratch
- Design end-to-end test strategies for real-world workflows
- Integrate test automation into CI pipelines
- Transition from low-code tools (Telerik/TestComplete) to **fully code-driven automation**

---

## CI/CD Integration
This project uses **GitHub Actions** to run tests automatically on pushes and pull requests.  
Benefits:
- Immediate feedback on failures
- Consistent test runs in CI
- HTML reports + logs can be uploaded as artifacts

---

## Project Structure

ecommerce-selenium-suite/
    data/ -> Test datasets (JSON)
    logs/ -> Execution logs
    pages/ -> POM classes
    reports/ -> HTML reports
    tests/ -> Test cases
    utils/ -> Helpers
    conftest.py -> Pytest fixtures
    requirements.txt 
    SETUP.md -> Setup details and instructions

---

## Technologies
- Python 3.x
- Selenium WebDriver
- pytest + pytest-html
- GitHub Actions (CI)

---

## Test Coverage
✔ Login (basic & data-driven)  
✔ Inventory browsing  
✔ Add to cart  
✔ End-to-end checkout  

Planned (Future Improvements):
- API-level validation
- Edge cases (empty cart checkout, out-of-stock items)

## Author
**Brandon Lacefield**  
QA Automation Engineer  
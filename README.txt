This project was created as part of a QA Automation Engineer portfolio to demonstrate code-first Selenium testing practices. While I have experience in QA automation using low-code tools like Telerik and TestComplete, this project bridges the gap to fully code-driven test suites using Python and Selenium.

### Goals:
- Simulate real-world E2E testing using Selenium
- Showcase scalable, maintainable automation practices
- Highlight abilities across data-driven testing, CI/CD readiness, and modular architecture

### Structure:
- `pages/`: Page Object Models (POM) for different parts of the site
- `tests/`: Organized test cases
- `data/`: Test data in JSON format
- `utils/`: Shared helper functions
- `logs/`: Holds 5 most recent logs per test (could be changed in the future for sake a storage)

### To Run:
```bash
pip install -r requirements.txt
pytest tests/name_of_test.py
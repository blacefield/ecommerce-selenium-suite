## How to Set Up and Run

### Prerequisites
- **Python 3.x** installed on your system
- Chrome-browser (along with Firefox and Edge for cross-browser tests) installation

### Installation
1. Clone the repository:
    git clone https://github.com/blacefield/ecommerce-selenium-suite.git
    cd ecommerce-selenium-suite

2. Install dependencies:
    pip install -r requirements.txt

### Running Tests
- Run a specific test from test file:
    pytest tests/e2e_checkout.py::TestE2ECheckoutFlow::test_single_item_e2e_purchase -v
- Run a specific test file:
    pytest tests/login.py -v
- Run all tests:
    pytest tests/ -v

### Running in CI
This suite is integrated with GitHub Actions.  
- Tests run automatically on each push and pull request (Can also be triggered manually).
- CI results can be viewed in the **Actions** tab of the GitHub repo. 
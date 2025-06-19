import json
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage

def create_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Load login test data
with open("data/login_data.json") as f:
    test_data = json.load(f)["users"]

@pytest.mark.parametrize("username,password", [(u["username"], u["password"]) for u in test_data])
def test_login_multiple_users(username, password):
    driver = create_driver(headless=True)
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(username, password)

    if "inventory" in driver.current_url:
        logging.info(f"[PASS] Login succeeded for user: {username}")
    else:
        try:
            error_el = driver.find_element(By.CLASS_NAME, "error-message-container")
            error_text = error_el.text.strip()
        except:
            error_text = "No error message found."

        logging.error(f"[FAIL] Login failed for user: {username} | Error: {error_text}")
        assert False, f"Login failed for {username} – {error_text}"

    driver.quit()
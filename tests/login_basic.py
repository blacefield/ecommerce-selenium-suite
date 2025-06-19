from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage

def test_login_success():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert "inventory" in driver.current_url
    driver.quit()
import json
from pages.login_page import LoginPage
from utils.drivers import create_driver

def login(browser="chrome",headless=True):
    """ Updated login function to upport cross-browser testing """
    
    with open("data/login_data.json") as f:
        creds = json.load(f)["users"][0]

    driver = create_driver(browser, headless)
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(creds["username"], creds["password"])
    assert "inventory" in driver.current_url
    return driver

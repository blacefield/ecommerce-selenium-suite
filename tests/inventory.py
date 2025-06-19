from pages.login_page import LoginPage
from utils.drivers import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def test_inventory_page_load():
    # Load credentials from JSON
    with open("data/login_data.json") as f:
        creds = json.load(f)["users"][0]  # using first user for this test (known working user, can be randomized in future)
        logger.info(f"Logged in as {creds['username']}")

    driver = create_driver()
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(creds["username"], creds["password"])

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    logger.info("Inventory items loaded successfully.")


    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    logger.info(f"Expected 6 inventory items, found {len(inventory_items)}")
    assert len(inventory_items) == 6, f"Expected 6 inventory items, found {len(inventory_items)}"

    first_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    first_item_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
    logger.info(f"First item name: {first_item_name}, price: {first_item_price}")

    assert first_item_name != "", "First item name should not be empty"
    assert "$" in first_item_price, "First item price should include a dollar sign"
    logger.info("All inventory checks passed !!!")

    driver.quit()
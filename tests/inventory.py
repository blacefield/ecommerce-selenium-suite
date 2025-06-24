from pages.login_page import LoginPage
from utils.drivers import create_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inventory_page import InventoryPage
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

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_inventory() 
    logger.info("Inventory items loaded successfully.")


    inventory_items = inventory_page.get_inventory_items()
    logger.info(f"Expected 6 inventory items, found {len(inventory_items)}")
    assert len(inventory_items) == 6, f"Expected 6 inventory items, found {len(inventory_items)}"

    first_item_name = inventory_page.get_first_item_name()
    first_item_price = inventory_page.get_first_item_price()
    logger.info(f"First item name: {first_item_name}, price: {first_item_price}")

    assert first_item_name != "", "First item name should not be empty"
    assert "$" in first_item_price, "First item price should include a dollar sign"
    logger.info("All inventory checks passed !!!")

    driver.quit()
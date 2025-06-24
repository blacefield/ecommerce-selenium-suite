import json
import logging
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.drivers import create_driver

# Initialize logger
logger = logging.getLogger(__name__) 

def test_add_single_item_to_cart():
    with open("data/login_data.json") as f:
        creds = json.load(f)["users"][0]

    driver = create_driver(False)
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(creds["username"], creds["password"])

    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_inventory()
    inventory_page.add_first_item_to_cart()

    cart_count = inventory_page.get_cart_count()
    logger.info(f"Cart Item Count: {cart_count}")
    assert cart_count == "1", f"Expected cart count 1, found {cart_count}"

    inventory_page.go_to_cart()
    cart_page = CartPage(driver)

    cart_page.wait_for_cart_items()
    cart_page_count = cart_page.cart_count()
    logger.info(f"Cart Page Item Count: {cart_page_count}")
    assert cart_page_count == 1, f"Expected 1 item in cart, found {cart_page_count}"

    driver.quit()
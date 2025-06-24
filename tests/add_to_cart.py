import logging
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from tests.login import login
import time

# Initialize logger
logger = logging.getLogger(__name__) 

def test_add_items_to_cart():
    driver = login()
    logger.info("Login Successful!!")

    items = ["shirt","car","backpack"]
    add_items_to_cart(driver, items)

    driver.quit()


def add_specific_item_to_cart(driver, item_to_add, num_cart_items=0):
    inventory_page = InventoryPage(driver)
    inventory_page.wait_for_inventory()
    added_bool = inventory_page.add_item_to_cart_by_name(item_to_add)
    if added_bool: 
        logger.info(f"Item containing '{item_to_add}' added to cart.")
    else:
        logger.info(f"Item containing '{item_to_add}' could NOT be found.")
        return added_bool    

    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    cart_page.wait_for_cart_items()
    expected_cart_count = num_cart_items + 1
    assert cart_page.cart_count() == expected_cart_count, f"Expected {expected_cart_count} item in cart, found {cart_page.cart_count()}"
    logger.info(f"{cart_page.cart_count()} items in the cart!!")

    cart_page.click_continue_shopping()
    return added_bool


def add_items_to_cart(driver, items_to_add):
    num_cart_items = 0

    for i, item in enumerate(items_to_add):
        added_bool = add_specific_item_to_cart(driver, item_to_add=item, num_cart_items=num_cart_items)
        if added_bool:
            num_cart_items += 1

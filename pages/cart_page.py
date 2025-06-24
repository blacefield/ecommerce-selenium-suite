from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.cart_item = (By.CLASS_NAME, "cart_item")
        self.checkout_button = (By.ID, "checkout")

    def wait_for_cart_items(self, wait_time=10):
        WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(self.cart_item)
        )

    def get_cart_items(self):
        return self.driver.find_elements(*self.cart_item)

    def click_checkout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        ).click()

    def cart_count(self):
        return len(self.get_cart_items())
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class InventoryPage:    
    def __init__(self, driver):        
        self.driver = driver            
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")        
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")    
        self.inventory_container = (By.CLASS_NAME, "inventory_list")
        self.inventory_items = (By.CLASS_NAME, "inventory_item")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def wait_for_inventory(self, wait_time=10):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(self.inventory_container)
            )
        except TimeoutException:
            raise Exception("Inventory did not load.")

    def get_inventory_items(self):
        return self.driver.find_elements(*self.inventory_items)

    def get_first_item_name(self):
        items = self.get_inventory_items()
        return items[0].find_element(By.CLASS_NAME, "inventory_item_name").text if items else ""

    def get_first_item_price(self):
        items = self.get_inventory_items()
        return items[0].find_element(By.CLASS_NAME, "inventory_item_price").text if items else ""

    def add_first_item_to_cart(self):
        items = self.get_inventory_items()
        if items:
            items[0].find_element(By.TAG_NAME, "button").click()

    def add_item_to_cart_by_name(self, name_fragment):
        items = self.get_inventory_items()
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            if name_fragment.lower() in name.lower():
                item.find_element(By.TAG_NAME, "button").click()
                return True
        return False

    def get_cart_count(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        except:
            return "0"

    def go_to_cart(self):
        self.driver.find_element(*self.cart_icon).click()
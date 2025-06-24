from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:    
    def __init__(self, driver):        
        self.driver = driver        
        self.inventory_item = (By.CLASS_NAME, "inventory_item")       
        self.first_item_name = (By.CLASS_NAME, "inventory_item_name")        
        self.first_item_price = (By.CLASS_NAME, "inventory_item_price")        
        self.add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")        
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")        
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")    
        
    def wait_for_inventory(self, wait_time = 10):        
        WebDriverWait(self.driver, wait_time).until(            
            EC.presence_of_all_elements_located(self.inventory_item)        
        )    
        
    def get_inventory_items(self):        
        return self.driver.find_elements(*self.inventory_item)    
    
    def get_first_item_name(self):        
        return self.driver.find_element(*self.first_item_name).text    
    
    def get_first_item_price(self):        
        return self.driver.find_element(*self.first_item_price).text    
    
    def add_first_item_to_cart(self):        
        self.driver.find_element(*self.add_to_cart_button).click()    
        
    def get_cart_count(self):        
        return self.driver.find_element(*self.cart_badge).text    
    
    def go_to_cart(self):        
        self.driver.find_element(*self.cart_link).click()
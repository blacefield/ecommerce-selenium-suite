from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        
        # Checkout Information
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.error_container = (By.CLASS_NAME, "error-message-container")
        
        # Checkout Overview
        self.item_total = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax_total = (By.CLASS_NAME, "summary_tax_label")
        self.total_price = (By.CLASS_NAME, "summary_total_label")
        self.finish_button = (By.ID, "finish")
        self.cart_items_overview = (By.CLASS_NAME, "cart_item")
        
        # Checkout Complete
        self.complete_header = (By.CLASS_NAME, "complete-header")
        self.complete_text = (By.CLASS_NAME, "complete-text")
        self.back_home_button = (By.ID, "back-to-products")

    def wait_for_checkout_info_page(self, wait_time=10):
        """Wait for the checkout information form to load"""
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(self.first_name_input)
            )
            return True
        except TimeoutException:
            return False

    def fill_checkout_information(self, first_name, last_name, postal_code):
        """Fill out the checkout information form"""
        self.driver.find_element(*self.first_name_input).clear()
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        
        self.driver.find_element(*self.last_name_input).clear()
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        
        self.driver.find_element(*self.postal_code_input).clear()
        self.driver.find_element(*self.postal_code_input).send_keys(postal_code)

    def click_continue(self):
        """Click the continue button to proceed to overview"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_button)
        ).click()

    def get_error_message(self):
        """Get error message if form validation fails"""
        try:
            error_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.error_container)
            )
            return error_element.text.strip()
        except TimeoutException:
            return None

    def wait_for_checkout_overview(self, wait_time=10):
        """Wait for the checkout overview page to load"""
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(self.item_total)
            )
            return True
        except TimeoutException:
            return False

    def get_item_total(self):
        """Get the subtotal amount from overview page"""
        try:
            total_text = self.driver.find_element(*self.item_total).text
            # Extract number from "Item total: $29.99" format
            return float(total_text.split('$')[1])
        except (ValueError, IndexError):
            return 0.0

    def get_tax_amount(self):
        """Get the tax amount from overview page"""
        try:
            tax_text = self.driver.find_element(*self.tax_total).text
            # Extract number from "Tax: $2.40" format
            return float(tax_text.split('$')[1])
        except (ValueError, IndexError):
            return 0.0

    def get_total_price(self):
        """Get the final total price from overview page"""
        try:
            total_text = self.driver.find_element(*self.total_price).text
            # Extract number from "Total: $32.39" format
            return float(total_text.split('$')[1])
        except (ValueError, IndexError):
            return 0.0

    def get_overview_items_count(self):
        """Get the number of items in the checkout overview"""
        try:
            items = self.driver.find_elements(*self.cart_items_overview)
            return len(items)
        except:
            return 0

    def click_finish(self):
        """Click the finish button to complete the purchase"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.finish_button)
        ).click()

    def wait_for_checkout_complete(self, wait_time=10):
        """Wait for the checkout complete page to load"""
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(self.complete_header)
            )
            return True
        except TimeoutException:
            return False

    def get_completion_message(self):
        """Get the order completion header message"""
        try:
            return self.driver.find_element(*self.complete_header).text
        except:
            return ""

    def get_completion_text(self):
        """Get the order completion description text"""
        try:
            return self.driver.find_element(*self.complete_text).text
        except:
            return ""

    def click_back_home(self):
        """Click back to products button to return to inventory"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.back_home_button)
        ).click()

    def is_on_checkout_info_page(self):
        """Check if currently on checkout information page"""
        try:
            self.driver.find_element(*self.first_name_input)
            return True
        except:
            return False

    def is_on_checkout_overview_page(self):
        """Check if currently on checkout overview page"""
        try:
            self.driver.find_element(*self.item_total)
            return True
        except:
            return False

    def is_on_checkout_complete_page(self):
        """Check if currently on checkout complete page"""
        try:
            self.driver.find_element(*self.complete_header)
            return True
        except:
            return False
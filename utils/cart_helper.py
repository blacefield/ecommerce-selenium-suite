import logging
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)

class CartHelper:
    """Helper class for cart operations to promote code reusability"""
    
    def __init__(self, driver):
        self.driver = driver
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)

    def add_items_to_cart(self, items_list):
        """
        Add multiple items to cart and return success status
        
        Args:
            items_list (list): List of item name fragments to add to cart
            
        Returns:
            dict: {
                'success': bool,
                'added_items': list,
                'failed_items': list,
                'total_added': int,
                'cart_count': int,
                'cart_count_matches': bool
            }
        """
        added_items = []
        failed_items = []
        
        # Ensure we're on inventory page
        self.inventory_page.wait_for_inventory()
        
        for item in items_list:
            success = self.inventory_page.add_item_to_cart_by_name(item)
            
            if success:
                added_items.append(item)
                logger.info(f"Successfully added item containing '{item}' to cart")
            else:
                failed_items.append(item)
                logger.warning(f"Failed to add item containing '{item}' - item not found")
        
        # Verify cart count matches added items
        expected_count = len(added_items)
        actual_count = int(self.inventory_page.get_cart_count())
        
        logger.info(f"Cart summary: {actual_count} items in cart, expected {expected_count}")
        
        return {
            'success': len(failed_items) == 0,
            'added_items': added_items,
            'failed_items': failed_items,
            'total_added': len(added_items),
            'cart_count': actual_count,
            'cart_count_matches': actual_count == expected_count
        }

    def verify_cart_contents(self, expected_count):
        """
        Navigate to cart and verify contents
        
        Args:
            expected_count (int): Expected number of items in cart
            
        Returns:
            dict: {
                'success': bool,
                'actual_count': int,
                'expected_count': int
            }
        """
        # Go to cart page
        self.inventory_page.go_to_cart()
        
        # Wait for cart items to load
        try:
            self.cart_page.wait_for_cart_items()
            actual_count = self.cart_page.cart_count()
        except:
            # If no items, cart_count should be 0
            actual_count = 0
        
        success = actual_count == expected_count
        
        logger.info(f"Cart verification: Expected {expected_count}, found {actual_count} - {'✓' if success else '✗'}")
        
        return {
            'success': success,
            'actual_count': actual_count,
            'expected_count': expected_count
        }

    def proceed_to_checkout(self):
        """
        Proceed from cart to checkout
        
        Returns:
            bool: True if successfully navigated to checkout
        """
        try:
            # Ensure we're on cart page
            if "cart" not in self.driver.current_url:
                self.inventory_page.go_to_cart()
                self.cart_page.wait_for_cart_items()
            
            # Click checkout button
            self.cart_page.click_checkout()
            
            # Verify we're on checkout page
            success = "checkout-step-one" in self.driver.current_url
            
            if success:
                logger.info("Successfully navigated to checkout page")
            else:
                logger.error("Failed to navigate to checkout page")
            
            return success
            
        except Exception as e:
            logger.error(f"Error proceeding to checkout: {str(e)}")
            return False

    def return_to_shopping(self):
        """
        Return to shopping from cart page
        
        Returns:
            bool: True if successfully returned to inventory
        """
        try:
            if "cart" not in self.driver.current_url:
                self.inventory_page.go_to_cart()
            
            self.cart_page.click_continue_shopping()
            
            success = "inventory" in self.driver.current_url
            
            if success:
                logger.info("Successfully returned to inventory page")
            else:
                logger.error("Failed to return to inventory page")
            
            return success
            
        except Exception as e:
            logger.error(f"Error returning to shopping: {str(e)}")
            return False

    def get_cart_summary(self):
        """
        Get comprehensive cart summary
        
        Returns:
            dict: Cart summary information
        """
        # Get cart count from inventory page badge
        inventory_cart_count = int(self.inventory_page.get_cart_count())
        
        # Navigate to cart and get detailed info
        self.inventory_page.go_to_cart()
        
        try:
            self.cart_page.wait_for_cart_items()
            cart_page_count = self.cart_page.cart_count()
        except:
            cart_page_count = 0
        
        summary = {
            'inventory_badge_count': inventory_cart_count,
            'cart_page_count': cart_page_count,
            'counts_match': inventory_cart_count == cart_page_count,
            'has_items': cart_page_count > 0
        }
        
        logger.info(f"Cart summary: Badge shows {inventory_cart_count}, cart page shows {cart_page_count}")
        
        return summary
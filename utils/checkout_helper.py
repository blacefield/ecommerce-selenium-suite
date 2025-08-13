import logging
from pages.checkout_page import CheckoutPage

logger = logging.getLogger(__name__)

class CheckoutHelper:
    """Helper class for checkout operations to promote code reusability"""
    
    def __init__(self, driver):
        self.driver = driver
        self.checkout_page = CheckoutPage(driver)

    def complete_checkout_information(self, first_name, last_name, postal_code):
        """
        Complete the checkout information step
        
        Args:
            first_name (str): Customer first name
            last_name (str): Customer last name  
            postal_code (str): Customer postal code
            
        Returns:
            dict: {
                'success': bool,
                'error_message': str or None,
                'step_completed': str
            }
        """
        try:
            # Verify we're on checkout info page
            if not self.checkout_page.wait_for_checkout_info_page():
                return {
                    'success': False,
                    'error_message': 'Checkout information page did not load',
                    'step_completed': None
                }
            
            # Fill out the form
            self.checkout_page.fill_checkout_information(first_name, last_name, postal_code)
            logger.info(f"Filled checkout info: {first_name} {last_name}, {postal_code}")
            
            # Click continue
            self.checkout_page.click_continue()
            
            # Check for validation errors
            error_message = self.checkout_page.get_error_message()
            if error_message:
                logger.error(f"Checkout info validation failed: {error_message}")
                return {
                    'success': False,
                    'error_message': error_message,
                    'step_completed': 'checkout_info_failed'
                }
            
            # Verify we moved to overview page
            if self.checkout_page.wait_for_checkout_overview():
                logger.info("Successfully completed checkout information step")
                return {
                    'success': True,
                    'error_message': None,
                    'step_completed': 'checkout_info'
                }
            else:
                return {
                    'success': False,
                    'error_message': 'Failed to proceed to checkout overview',
                    'step_completed': 'checkout_info_failed'
                }
                
        except Exception as e:
            error_msg = f"Exception during checkout info: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error_message': error_msg,
                'step_completed': 'checkout_info_error'
            }

    def verify_checkout_overview(self, expected_items_count=None):
        """
        Verify the checkout overview page details
        
        Args:
            expected_items_count (int, optional): Expected number of items
            
        Returns:
            dict: Overview verification results and totals
        """
        try:
            if not self.checkout_page.wait_for_checkout_overview():
                return {
                    'success': False,
                    'error': 'Checkout overview page did not load'
                }
            
            # Get all the totals
            item_total = self.checkout_page.get_item_total()
            tax_amount = self.checkout_page.get_tax_amount()
            final_total = self.checkout_page.get_total_price()
            items_count = self.checkout_page.get_overview_items_count()
            
            # Verify math (item total + tax = final total, within small rounding tolerance)
            calculated_total = item_total + tax_amount
            math_correct = abs(calculated_total - final_total) < 0.01
            
            # Verify expected items count if provided
            items_count_correct = True
            if expected_items_count is not None:
                items_count_correct = items_count == expected_items_count
            
            success = math_correct and items_count_correct and item_total > 0
            
            result = {
                'success': success,
                'item_total': item_total,
                'tax_amount': tax_amount,
                'final_total': final_total,
                'calculated_total': calculated_total,
                'math_correct': math_correct,
                'items_count': items_count,
                'expected_items_count': expected_items_count,
                'items_count_correct': items_count_correct
            }
            
            logger.info(f"Checkout overview - Items: {items_count}, Subtotal: ${item_total:.2f}, "
                       f"Tax: ${tax_amount:.2f}, Total: ${final_total:.2f}")
            
            if not math_correct:
                logger.error(f"Math error: ${item_total:.2f} + ${tax_amount:.2f} = ${calculated_total:.2f} "
                           f"but final shows ${final_total:.2f}")
            
            if expected_items_count and not items_count_correct:
                logger.error(f"Items count mismatch: expected {expected_items_count}, found {items_count}")
            
            return result
            
        except Exception as e:
            error_msg = f"Exception during overview verification: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def complete_purchase(self):
        """
        Complete the final purchase step
        
        Returns:
            dict: {
                'success': bool,
                'completion_message': str,
                'completion_text': str
            }
        """
        try:
            # Ensure we're on overview page
            if not self.checkout_page.is_on_checkout_overview_page():
                return {
                    'success': False,
                    'error': 'Not on checkout overview page'
                }
            
            # Click finish
            self.checkout_page.click_finish()
            logger.info("Clicked finish button")
            
            # Wait for completion page
            if not self.checkout_page.wait_for_checkout_complete():
                return {
                    'success': False,
                    'error': 'Checkout completion page did not load'
                }
            
            # Get completion messages
            completion_message = self.checkout_page.get_completion_message()
            completion_text = self.checkout_page.get_completion_text()
            
            logger.info(f"Purchase completed! Message: '{completion_message}'")
            
            return {
                'success': True,
                'completion_message': completion_message,
                'completion_text': completion_text,
                'step_completed': 'purchase_complete'
            }
            
        except Exception as e:
            error_msg = f"Exception during purchase completion: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def return_to_inventory(self):
        """
        Return to inventory from completion page
        
        Returns:
            bool: True if successfully returned to inventory
        """
        try:
            if not self.checkout_page.is_on_checkout_complete_page():
                logger.warning("Not on checkout complete page")
                return False
            
            self.checkout_page.click_back_home()
            
            success = "inventory" in self.driver.current_url
            
            if success:
                logger.info("Successfully returned to inventory from checkout complete")
            else:
                logger.error("Failed to return to inventory from checkout complete")
            
            return success
            
        except Exception as e:
            logger.error(f"Error returning to inventory: {str(e)}")
            return False

    def complete_full_checkout_flow(self, first_name, last_name, postal_code, expected_items_count=None):
        """
        Complete the entire checkout flow in one method
        
        Args:
            first_name (str): Customer first name
            last_name (str): Customer last name
            postal_code (str): Customer postal code
            expected_items_count (int, optional): Expected number of items
            
        Returns:
            dict: Complete checkout flow results
        """
        logger.info(f"Starting full checkout flow for {first_name} {last_name}")
        
        # Step 1: Complete checkout information
        info_result = self.complete_checkout_information(first_name, last_name, postal_code)
        if not info_result['success']:
            return {
                'success': False,
                'failed_step': 'checkout_info',
                'error': info_result['error_message'],
                'info_result': info_result
            }
        
        # Step 2: Verify checkout overview
        overview_result = self.verify_checkout_overview(expected_items_count)
        if not overview_result['success']:
            return {
                'success': False,
                'failed_step': 'checkout_overview',
                'error': overview_result.get('error', 'Overview verification failed'),
                'info_result': info_result,
                'overview_result': overview_result
            }
        
        # Step 3: Complete purchase
        purchase_result = self.complete_purchase()
        if not purchase_result['success']:
            return {
                'success': False,
                'failed_step': 'purchase_completion',
                'error': purchase_result.get('error', 'Purchase completion failed'),
                'info_result': info_result,
                'overview_result': overview_result,
                'purchase_result': purchase_result
            }
        
        # Success!
        logger.info("✅ Full checkout flow completed successfully!")
        
        return {
            'success': True,
            'info_result': info_result,
            'overview_result': overview_result,
            'purchase_result': purchase_result,
            'final_total': overview_result['final_total'],
            'items_purchased': overview_result['items_count']
        }
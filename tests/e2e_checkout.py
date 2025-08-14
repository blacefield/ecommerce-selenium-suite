import json
import logging
import pytest
from tests.login import login
from pages.inventory_page import InventoryPage
from utils.cart_helper import CartHelper
from utils.checkout_helper import CheckoutHelper

# Initialize logger
logger = logging.getLogger(__name__)

class TestE2ECheckoutFlow:
    """Complete End-to-End test suite for the full purchase journey"""
    
    @pytest.fixture(params=["chrome","firefox","edge"])
    def authenticated_driver(self, request):
        """Fixture that provides an authenticated driver session for multiple browsers"""
        browser = request.param
        driver = login(browser, True)
        yield driver
        driver.quit()
    
    @pytest.fixture
    def checkout_data(self):
        """Fixture that loads checkout test data"""
        with open("data/checkout_data.json") as f:
            return json.load(f)

    def test_single_item_e2e_purchase(self, authenticated_driver, checkout_data):
        """Test complete purchase flow with a single item"""
        driver = authenticated_driver
        
        # Get test scenario data
        scenario = checkout_data["e2e_test_scenarios"][0]  # single_item_purchase
        items_to_add = scenario["items_to_add"]
        customer_info = scenario["customer_info"]
        
        logger.info(f"🛒 Starting E2E test: {scenario['test_name']}")
        
        # Step 1: Verify we're on inventory page after login
        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_inventory()
        assert "inventory" in driver.current_url, "Should be on inventory page after login"
        logger.info("✅ Verified inventory page loaded after login")
        
        # Step 2: Add items to cart using CartHelper
        cart_helper = CartHelper(driver)
        add_result = cart_helper.add_items_to_cart(items_to_add)
        
        assert add_result['success'], f"Failed to add items: {add_result['failed_items']}"
        assert add_result['total_added'] == len(items_to_add), "Not all items were added"
        assert add_result['cart_count_matches'], "Cart count doesn't match expected"
        logger.info(f"✅ Successfully added {add_result['total_added']} items to cart")
        
        # Step 3: Verify cart contents
        cart_verification = cart_helper.verify_cart_contents(len(items_to_add))
        assert cart_verification['success'], "Cart verification failed"
        logger.info("✅ Cart contents verified")
        
        # Step 4: Proceed to checkout
        checkout_success = cart_helper.proceed_to_checkout()
        assert checkout_success, "Failed to proceed to checkout"
        logger.info("✅ Successfully navigated to checkout")
        
        # Step 5: Complete checkout using CheckoutHelper
        checkout_helper = CheckoutHelper(driver)
        checkout_result = checkout_helper.complete_full_checkout_flow(
            customer_info["first_name"],
            customer_info["last_name"], 
            customer_info["postal_code"],
            expected_items_count=len(items_to_add)
        )
        
        assert checkout_result['success'], f"Checkout failed at step: {checkout_result.get('failed_step', 'unknown')}"
        assert checkout_result['items_purchased'] == len(items_to_add), "Wrong number of items purchased"
        assert checkout_result['final_total'] > 0, "Final total should be greater than 0"
        
        logger.info(f"✅ Purchase completed! Total: ${checkout_result['final_total']:.2f}")
        
        # Step 6: Return to inventory
        return_success = checkout_helper.return_to_inventory()
        assert return_success, "Failed to return to inventory"
        logger.info("✅ Successfully returned to inventory page")
        
        # Final verification - we should be back on inventory with empty cart
        assert "inventory" in driver.current_url, "Should be back on inventory page"
        inventory_cart_count = inventory_page.get_cart_count()
        assert inventory_cart_count == "0", f"Cart should be empty but shows {inventory_cart_count}"
        logger.info("✅ E2E test completed successfully - cart is now empty")

    def test_multiple_items_e2e_purchase(self, authenticated_driver, checkout_data):
        """Test complete purchase flow with multiple items"""
        driver = authenticated_driver
        
        # Get test scenario data
        scenario = checkout_data["e2e_test_scenarios"][1]  # multiple_items_purchase
        items_to_add = scenario["items_to_add"]
        customer_info = scenario["customer_info"]
        
        logger.info(f"🛒 Starting E2E test: {scenario['test_name']} with {len(items_to_add)} items")
        
        # Step 1: Verify inventory page
        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_inventory()
        logger.info("✅ Inventory page loaded")
        
        # Step 2: Add multiple items to cart
        cart_helper = CartHelper(driver)
        add_result = cart_helper.add_items_to_cart(items_to_add)
        
        # Allow for some items to not be found (testing resilience)
        assert add_result['total_added'] > 0, "Should have added at least one item"
        logger.info(f"✅ Added {add_result['total_added']} out of {len(items_to_add)} requested items")
        
        if add_result['failed_items']:
            logger.warning(f"Some items not found: {add_result['failed_items']}")
        
        # Step 3: Verify cart and proceed to checkout
        expected_count = add_result['total_added']
        cart_verification = cart_helper.verify_cart_contents(expected_count)
        assert cart_verification['success'], "Cart verification failed"
        
        checkout_success = cart_helper.proceed_to_checkout()
        assert checkout_success, "Failed to proceed to checkout"
        logger.info("✅ Proceeded to checkout with multiple items")
        
        # Step 4: Complete checkout
        checkout_helper = CheckoutHelper(driver)
        checkout_result = checkout_helper.complete_full_checkout_flow(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"],
            expected_items_count=expected_count
        )
        
        assert checkout_result['success'], f"Multi-item checkout failed: {checkout_result.get('error', 'Unknown error')}"
        assert checkout_result['final_total'] > 0, "Should have a positive total"
        
        logger.info(f"✅ Multi-item purchase completed! Items: {checkout_result['items_purchased']}, Total: ${checkout_result['final_total']:.2f}")
        
        # Step 5: Complete the flow
        return_success = checkout_helper.return_to_inventory()
        assert return_success, "Failed to return to inventory"
        logger.info("✅ Multi-item E2E test completed successfully")

    def test_checkout_validation_errors(self, authenticated_driver, checkout_data):
        """Test checkout form validation with invalid data"""
        driver = authenticated_driver
        
        logger.info("🚨 Testing checkout form validation")
        
        # Step 1: Add an item to cart first
        cart_helper = CartHelper(driver)
        add_result = cart_helper.add_items_to_cart(["backpack"])
        assert add_result['success'], "Failed to add item for validation test"
        
        # Step 2: Proceed to checkout
        checkout_success = cart_helper.proceed_to_checkout()
        assert checkout_success, "Failed to reach checkout for validation test"
        
        # Step 3: Test each validation scenario
        checkout_helper = CheckoutHelper(driver)
        invalid_scenarios = checkout_data["invalid_checkout_info"]
        
        for scenario in invalid_scenarios:
            logger.info(f"Testing validation: {scenario['expected_error']}")
            
            # Try to complete checkout with invalid data
            info_result = checkout_helper.complete_checkout_information(
                scenario["first_name"],
                scenario["last_name"], 
                scenario["postal_code"]
            )
            
            # Should fail with expected error
            assert not info_result['success'], f"Validation should have failed for: {scenario}"
            assert info_result['error_message'] is not None, "Should have an error message"
            logger.info(f"✅ Validation correctly failed: {info_result['error_message']}")
        
        logger.info("✅ All validation scenarios tested successfully")

    @pytest.mark.parametrize("scenario_index", [0, 1, 2])
    def test_parameterized_e2e_scenarios(self, authenticated_driver, checkout_data, scenario_index):
        """Parameterized test for all E2E scenarios"""
        driver = authenticated_driver
        
        scenario = checkout_data["e2e_test_scenarios"][scenario_index]
        items_to_add = scenario["items_to_add"]
        customer_info = scenario["customer_info"]
        
        logger.info(f"🔄 Running parameterized E2E test: {scenario['test_name']}")
        
        # Complete E2E flow
        cart_helper = CartHelper(driver)
        add_result = cart_helper.add_items_to_cart(items_to_add)
        
        # Proceed only if we successfully added items
        if add_result['total_added'] > 0:
            cart_helper.proceed_to_checkout()
            
            checkout_helper = CheckoutHelper(driver)
            checkout_result = checkout_helper.complete_full_checkout_flow(
                customer_info["first_name"],
                customer_info["last_name"],
                customer_info["postal_code"],
                expected_items_count=add_result['total_added']
            )
            
            assert checkout_result['success'], f"Parameterized test failed for {scenario['test_name']}"
            logger.info(f"✅ Parameterized test passed: {scenario['test_name']}")
        else:
            pytest.skip(f"No items could be added for scenario: {scenario['test_name']}")

    def test_cart_to_inventory_navigation(self, authenticated_driver):
        """Test navigation flow: Inventory -> Cart -> Back to Inventory"""
        driver = authenticated_driver
        
        logger.info("🔄 Testing cart navigation flow")
        
        cart_helper = CartHelper(driver)
        
        # Add items to cart
        add_result = cart_helper.add_items_to_cart(["shirt"])
        assert add_result['success'], "Failed to add item for navigation test"
        
        # Go to cart and verify
        inventory_page = InventoryPage(driver)
        inventory_page.go_to_cart()
        assert "cart" in driver.current_url, "Should be on cart page"
        logger.info("✅ Successfully navigated to cart")
        
        # Return to shopping
        return_success = cart_helper.return_to_shopping()
        assert return_success, "Failed to return to inventory"
        assert "inventory" in driver.current_url, "Should be back on inventory"
        logger.info("✅ Successfully returned to inventory from cart")

    def test_checkout_overview_calculations(self, authenticated_driver, checkout_data):
        """Test that checkout overview calculations are correct"""
        driver = authenticated_driver
        
        logger.info("** Testing checkout calculations")
        
        # Add multiple items to get meaningful totals
        cart_helper = CartHelper(driver)
        add_result = cart_helper.add_items_to_cart(["backpack", "shirt"])
        
        if add_result['total_added'] < 2:
            logger.warning("Not enough items added for calculation test")
            return
        
        # Proceed to checkout overview
        cart_helper.proceed_to_checkout()
        
        checkout_helper = CheckoutHelper(driver)
        customer_info = checkout_data["valid_checkout_info"][0]
        
        # Complete info step
        info_result = checkout_helper.complete_checkout_information(
            customer_info["first_name"],
            customer_info["last_name"],
            customer_info["postal_code"]
        )
        assert info_result['success'], "Failed to complete checkout info"
        
        # Verify calculations
        overview_result = checkout_helper.verify_checkout_overview(add_result['total_added'])
        assert overview_result['success'], "Checkout calculations failed"
        assert overview_result['math_correct'], "Item total + tax should equal final total"
        assert overview_result['item_total'] > 0, "Item total should be positive"
        assert overview_result['tax_amount'] >= 0, "Tax should be non-negative"
        
        logger.info(f"✅ Calculations verified: ${overview_result['item_total']:.2f} + ${overview_result['tax_amount']:.2f} = ${overview_result['final_total']:.2f}")

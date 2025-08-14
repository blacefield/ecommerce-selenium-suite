from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def create_driver(browser="chrome", headless=True):
    """
    Create a WebDriver instance for cross-browser testing.
    
    Args:
        browser (str): "chrome", "firefox", or "edge"
    """
    browser = browser.lower()
    
    if browser == "chrome":
        return _create_chrome_driver(headless)
    elif browser == "firefox":
        return _create_firefox_driver(headless)
    elif browser == "edge":
        return _create_edge_driver(headless)
    else:
        raise ValueError(f"Unsupported browser: {browser}. Use 'chrome', 'firefox', or 'edge'")

def _create_chrome_driver(headless=True):
    """Create Chrome WebDriver with options."""
    options = ChromeOptions()
    
    if headless:
        options.add_argument("--headless=new")
    
    # Common Chrome arguments
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Prevents "Change your password" prompt in Chrome
    preferences = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", preferences)
    
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def _create_firefox_driver(headless=True):
    """Create Firefox WebDriver with options."""
    options = FirefoxOptions()
    
    if headless:
        options.add_argument("--headless")
    
    # Set window size for Firefox
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    
    # Firefox preferences
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("media.volume_scale", "0.0")
    
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def _create_edge_driver(headless=True):
    """Create Edge WebDriver with options."""
    options = EdgeOptions()
    
    if headless:
        options.add_argument("--headless=new")
    
    # Common Edge arguments (similar to Chrome since Edge is Chromium-based)
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Prevents password manager prompts
    preferences = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", preferences)
    
    service = EdgeService("C:\WebDrivers\msedgedriver.exe") #(EdgeChromiumDriverManager().install())  Getting issues installing msedgedriver here so pointed it to the local version
    return webdriver.Edge(service=service, options=options)

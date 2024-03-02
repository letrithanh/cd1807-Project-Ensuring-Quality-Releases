from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{timestamp} - {message}")


def driver_instance():
    log("Start Chrome")
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9222")

    return webdriver.Chrome(options=options)


def run():
    driver = driver_instance()
    
    login(driver, "standard_user", "secret_sauce")
    add_cart(driver)
    remove_cart(driver)


def login (driver, user, password):
    log("Login")
    log("Visit https://www.saucedemo.com/")
    driver.get("https://www.saucedemo.com/")

    log(f"Enter username {user}")
    driver.find_element(By.CSS_SELECTOR, "input[id = 'user-name']").send_keys(user)

    log(f"Enter password {password}")
    driver.find_element(By.CSS_SELECTOR, "input[id = 'password']").send_keys(password)

    log("Click button")
    driver.find_element(By.CSS_SELECTOR, "input[id = 'login-button']").click()

    logo = driver.find_elements(By.CSS_SELECTOR, ".app_logo")
    assert len(logo) > 0, "App logo not found"

    log("Success login")


def add_cart(driver):
    log("Add product")
    products = driver.find_elements(By.CSS_SELECTOR, ".inventory_item")

    for product in products:
        product_button = product.find_element(By.CSS_SELECTOR, ".btn_inventory")
        product_name = product.find_element(By.CSS_SELECTOR, ".inventory_item_name")
        product_button.click()

        log(f"Added {product_name.text}")

    cart = int(driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text)
    assert cart == len(products), "Adding failed"

    log(f"Cart: {cart}")


def remove_cart(driver):
    log("Remove cart")
    driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()

    log("Clear products")
    remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".cart_button")
    for remove_button in remove_buttons:
        remove_button.click()

    cart = driver.find_elements(By.CSS_SELECTOR, ".shopping_cart_badge")
    assert len(cart) == 0, "Removing failed"

    log("Removed cart")

run()
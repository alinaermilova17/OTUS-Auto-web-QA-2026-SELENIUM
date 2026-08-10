import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

os.makedirs('/app/screenshots', exist_ok=True)

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Remote(
    command_executor='http://selenium-chrome:4444/wd/hub',
    options=options
)
print("=" * 60)
print("ГЛАВНАЯ СТРАНИЦА")
print("=" * 60)
driver.get('http://prestashop:80')
time.sleep(3)
driver.save_screenshot('/app/screenshots/1_main_page.png')

selectors_main = {
    'ADD_TO_CART_FROM_MAIN_PAGE': "button[data-button-action='add-to-cart']",
    'ITEM_TO_CART': '.cart-products-count',
    'CART_ITEM': '.cart-products-count',
    'CART_LABEL': '#_desktop_cart .hidden-sm-down',
}

print("\n--- Поиск на главной странице ---")
for name, selector in selectors_main.items():
    try:
        el = driver.find_element(By.CSS_SELECTOR, selector)
        print(f"✅ НАЙДЕН: {name} -> {selector}")
        print(f"   text='{el.text.strip()}', class='{el.get_attribute('class')}'")
    except:
        print(f"❌ НЕ НАЙДЕН: {name} -> {selector}")

print("\n" + "=" * 60)
print("СТРАНИЦА ТОВАРА")
print("=" * 60)
driver.get('http://prestashop:80/men/1-hummingbird-printed-t-shirt.html')
time.sleep(5)
driver.save_screenshot('/app/screenshots/2_product_page.png')

with open('/app/screenshots/product_page.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

selectors_product = {
    'ADD_TO_CART_BUTTON': 'add-to-cart-or-refresh > div.product-add-to-cart.js-product-add-to-cart > div > div.add > button',
    'ADD_TO_CART_BUTTON_v2': '.product-add-to-cart button',
    'ADD_TO_CART_BUTTON_v3': '#add-to-cart-or-refresh button',
    'ADD_TO_CART_BUTTON_v4': 'button.add-to-cart',
    'ADD_TO_CART_BUTTON_v5': '.btn-primary.add-to-cart',
    'ADD_TO_CART_BUTTON_v6': '[data-button-action="add-to-cart"]',
    'QUANTITY': "//div[contains(@class, 'qty')]//input[@type='number']",
    'PRODUCT_IMAGE': "img[alt='Hummingbird printed t-shirt']",
    'PRODUCT_IMAGE_v2': "img[alt*='Hummingbird']",
    'PRODUCT_IMAGE_v3': ".product-cover img",
}

print("\n--- Поиск на странице товара ---")
for name, selector in selectors_product.items():
    try:
        if selector.startswith('//'):
            el = driver.find_element(By.XPATH, selector)
        else:
            el = driver.find_element(By.CSS_SELECTOR, selector)
        print(f"✅ НАЙДЕН: {name} -> {selector}")
        print(f"   text='{el.text.strip()}', class='{el.get_attribute('class')}'")
    except:
        print(f"❌ НЕ НАЙДЕН: {name} -> {selector}")

print("\n--- ВСЕ КНОПКИ НА СТРАНИЦЕ ТОВАРА ---")
buttons = driver.find_elements(By.TAG_NAME, 'button')
for i, btn in enumerate(buttons):
    try:
        print(f"BTN #{i}: text='{btn.text.strip()}'")
        print(f"        class='{btn.get_attribute('class')}'")
        print(f"        data-action='{btn.get_attribute('data-button-action')}'")
        print(f"        id='{btn.get_attribute('id')}'")
        outer = btn.get_attribute('outerHTML')[:200]
        print(f"        HTML: {outer}")
        print("---")
    except:
        pass

print("\n--- ЭЛЕМЕНТЫ С CLASS*='add' или CLASS*='cart' ---")
elements = driver.find_elements(By.CSS_SELECTOR, '[class*="add"], [class*="cart"], [id*="add"], [id*="cart"]')
for el in elements[:15]:
    try:
        print(f"<{el.tag_name}> class='{el.get_attribute('class')}' id='{el.get_attribute('id')}' text='{el.text[:80]}'")
    except:
        pass

print("  - screenshots/1_main_page.png")
print("  - screenshots/2_product_page.png")
print("  - screenshots/product_page.html")

driver.quit()
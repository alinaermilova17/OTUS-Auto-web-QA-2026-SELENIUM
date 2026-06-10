from selenium.webdriver.common.by import By


class MainPage:
    USER_BUTTON = (By.CSS_SELECTOR, "_mobile_user_info > div > a > i")
    SUBSCRIBE_BUTTON = (By.CSS_SELECTOR, "blockEmailSubscription_displayFooterBefore > div > div > form > div > div:nth-child(1) > input.btn.btn-primary.float-xs-right.hidden-xs-down")
    MOBILE_CART = (By.CSS_SELECTOR,  "_mobile_cart > div")
    DESKTOP_LOGO = (By.CSS_SELECTOR, "_desktop_logo")
    SEARCH_FIELD = (By.CSS_SELECTOR, "search_widget > form > input.ui-autocomplete-input")
    CURRENCY_SELECTOR = (By.CSS_SELECTOR, ".expand-more._gray-darker")
    USD_OPTION = (By.CSS_SELECTOR, "a[title='US Dollar']")
    EXPAND_ICON = (By.CSS_SELECTOR, "i.material-icons.expand-more")
    CURRENCY_BUTTON = (By.CSS_SELECTOR, ".expand-more._gray-darker")
    USD_PRICE = (By.CSS_SELECTOR, "span.price[aria-label='Price']")
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PageHomeShopLocator:
    CHANGE_CURRENCY = (By.CSS_SELECTOR, '[class="btn btn-link dropdown-toggle"]')


class PageHomeShop(BasePage):
    def click_menu_change_currency(self):
        with allure.step("Значек смены валюты"):
            self.find_element(PageHomeShopLocator.CHANGE_CURRENCY).click()

    def change_currency(self, currency):
        with allure.step("Выбор валюты"):
            self.find_element((By.CSS_SELECTOR, f'[name="{currency}"]')).click()

    def get_text_icon_currency(self):
        with allure.step("Текст икноки валюты"):
            return self.find_element((By.CSS_SELECTOR, '[class="btn btn-link dropdown-toggle"] strong')).text

    def get_price_macbook(self):
        with allure.step("Получаем цену товара"):
            return self.find_element((By.XPATH, "//*[text()='MacBook']/../../p[@class='price']")).get_property("outerText")

    def get_count_product_by_page(self):
        with allure.step("Получаем количество товаров на странице"):
            return len(self.find_elements((By.CSS_SELECTOR, '[class="product-thumb transition"]')))

    def get_text_footer(self):
        return self.find_element((By.CSS_SELECTOR, 'footer p')).get_property("textContent")

    def count_currency(self):
        with allure.step("Получаем количество доступных валют"):
            return len(self.find_elements((By.CSS_SELECTOR, '[class="currency-select btn btn-link btn-block"]')))

    def get_text_by_search_placeholder(self):
        return self.find_element((By.CSS_SELECTOR, '[name="search"]')).get_attribute("placeholder")

    def get_text_by_button_basket(self):
        return self.find_element((By.CSS_SELECTOR, '[id="cart-total"]')).text

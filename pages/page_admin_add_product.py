from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class PageAddProductLocator:
    SAVE = (By.CSS_SELECTOR, '[form="form-product"]')


class PageAddProduct(BasePage):
    def fill_name_title_model(self, name, title, model):
        self.find_element((By.CSS_SELECTOR, '[id="input-name1"]')).send_keys(name)
        self.find_element((By.CSS_SELECTOR, '[id="input-meta-title1"]')).send_keys(title)
        self.find_element((By.XPATH, "//*[text()='Data']")).click()
        self.find_element((By.CSS_SELECTOR, '[id="input-model"]')).send_keys(model)

    def click_save_product_button(self):
        self.find_element(PageAddProductLocator.SAVE).click()



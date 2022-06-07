from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class PageHomeAdminLocator:
    ADD_PRODUCT = (By.CSS_SELECTOR, '[class ="fa fa-plus"]')
    ALERT = (By.CSS_SELECTOR, '[class ="alert alert-success alert-dismissible"]')


class PageHomeAdmin(BasePage):
    def open_page_products(self):
        with allure.step("Переходим на страницу продукты"):
            self.find_element((By.CSS_SELECTOR, '[id="menu-catalog"]')).click()
            self.find_element((By.XPATH, "//*[text()='Products']")).click()

    def open_menu_add_product(self):
        with allure.step("Переходим на страницу добавления продукта"):
            self.find_element(PageHomeAdminLocator.ADD_PRODUCT).click()

    def text_alert(self):
        return self.find_element(PageHomeAdminLocator.ALERT).text

    def count_product(self):
        with allure.step("Получаем количество товаров на странице"):
            count = self.find_element((By.CSS_SELECTOR, '[class ="col-sm-6 text-right"]')).text
            count = count[count.find("of") + 3:].partition(' ')[0]
            return int(count)

    def change_checkbox_by_name_product(self, name_product):
        with allure.step("ВЫбираем товар - нажимаем чекбокс"):
            self.find_element((By.XPATH, f"//*[text()='{name_product}']/..//input")).click()

    def click_delete_button(self):
        with allure.step("Удаляем товар"):
            self.find_element((By.CSS_SELECTOR, '[data-original-title="Delete"]')).click()
            confirm = self.browser.switch_to.alert
            confirm.accept()

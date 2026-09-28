from selenium.webdriver.common.by import By

from base.base_page import BasePage


class SearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_loc = By.XPATH,'//android.widget.TextSwitcher[@resource-id="com.netease.yanxuan:id/tv_home_search"]'
        self.search_input_loc = By.ID,'com.netease.yanxuan:id/search_input'
        self.search_button_loc = By.ID,'com.netease.yanxuan:id/tv_search_button'
        self.first_result_loc = By.XPATH,'(//android.widget.TextView[@resource-id="com.netease.yanxuan:id/tv_goods_name"])[1]'

    def search(self,keyword):
        self.base_click(self.search_loc)
        self.base_input_text(self.search_input_loc,keyword)
        self.base_click(self.search_button_loc)

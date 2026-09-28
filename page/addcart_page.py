from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from base.base_page import BasePage
from base import logger

class AddCartPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.good_loc = By.XPATH,'(//android.widget.GridView/android.widget.LinearLayout[@resource-id="com.netease.yanxuan:id/good"])[1]'
        self.addcart_button_loc = By.XPATH,'//android.widget.TextView[@resource-id="com.netease.yanxuan:id/button" and @text="加入购物车"]'
        self.location_agree_button_loc = By.ID,'com.netease.yanxuan:id/btn_alert_positive'
        self.addcart_button_confirm_loc = By.ID,'com.netease.yanxuan:id/button'
        self.return_search_success_loc = By.ID,'com.netease.yanxuan:id/nav_left_text'
        self.return_search_bar_loc = By.ID,'com.netease.yanxuan:id/search_bar_return'
        self.return_home_loc = By.ID,'com.netease.yanxuan:id/search_bar_return'
        self.success_toast_loc = By.XPATH,'//android.widget.Toast'

    def enter_goods_details(self):
        self.base_click(self.good_loc)

        try:
            WebDriverWait(self.driver, 2).until(
                ec.element_to_be_clickable(self.location_agree_button_loc)
            ).click()
        except TimeoutException:
            logger.info("未出现位置确认弹窗，继续执行")

    def add_cart(self):
        self.base_click(self.addcart_button_loc)
        self.base_click(self.addcart_button_confirm_loc)
        toast = self.base_get_toast(self.success_toast_loc)
        self.base_get_shot(f"添加购物车_{toast or '未捕获Toast'}")
        return toast

    def back_to_home(self):
        self.base_click(self.return_search_success_loc)
        self.base_click(self.return_search_bar_loc)
        self.base_click(self.return_home_loc)

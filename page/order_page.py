from selenium.webdriver.common.by import By

from base.base_page import BasePage


class OrderPage(BasePage):
    def __init__(self , driver):
        super().__init__(driver)
        self.cart_button_loc = By.XPATH,('//android.widget.TextView'
                                         '[@resource-id="com.netease.yanxuan:id/txt_mainpage_tab_title" and @text="购物车"]')
        self.order_button_loc = By.XPATH,'//android.widget.TextView[contains(@text,"结算")]'
        self.all_order_loc = By.XPATH,'//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]'

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from base import logger
from base.base_page import BasePage
from selenium.webdriver.common.by import By


class EnterHomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.agree_loc = By.ID, 'com.netease.yanxuan:id/btn_alert_positive'
        self.skip_loc = By.XPATH,'//android.widget.TextView[@text="跳过"]'

    def agree_eula(self):
        self.base_click(self.agree_loc)

    def skip_ad(self, timeout=2):
        try:
            button = WebDriverWait(self.driver, timeout).until(
                ec.element_to_be_clickable(self.skip_loc)
            )
        except TimeoutException:
            logger.info("未出现启动广告的跳过按钮，继续执行")
            return False
        button.click()
        return True
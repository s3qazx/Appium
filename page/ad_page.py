from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from base import logger
from base.base_page import BasePage
from page import login_page


class AdPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.remove_add_button_loc = By.XPATH,'//*[@resource-id="com.netease.yanxuan:id/trans_cancel"]/android.widget.ImageView'

    def remove_add(self,locator,timeout = 2):
        try:
            close_button= WebDriverWait(self.driver,timeout).until(
                ec.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.info("未发现可点击的广告关闭按钮，继续执行")
            return False

        close_button.click()
        return True
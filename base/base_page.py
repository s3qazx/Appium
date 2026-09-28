import os
import re
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from base import logger
from config import BASE_DIR

class BasePage :
    def __init__(self , driver):
        self.driver = driver

    def fd_element(self , locator,timeout=3):
        try:
            logger.info(f"定位元素:{locator}")
            element = WebDriverWait(self.driver , timeout).until(
                ec.visibility_of_element_located(locator))
            return element
        except Exception as e :
            logger.error(f"元素定位失败:{locator}-{str(e)}")
            raise

    def base_click(self,locator):
        logger.info(f"点击元素:{locator}")
        self.fd_element(locator).click()

    def base_input_text(self,locator,text):
        logger.info(f"在元素:{locator}输入文本")
        element = self.fd_element(locator)
        element.clear()
        element.send_keys(text)

    def base_get_text(self,locator):
        text = self.fd_element(locator).text
        logger.info(f"获取元素文本:{locator} -> {text}")
        return text

    def base_swipe(self,start_X,start_Y,end_X,end_Y,duration=1000):
        logger.info(f"滑动操作:({start_X},{start_Y})->({end_X},{end_Y}),{duration}")
        self.driver.swipe(start_X,start_Y,end_X,end_Y,duration)

    def base_get_toast(self, toast_loc, timeout=5):
        try:
            # 在轮询内直接读取文字，节点消失或暂时无文字时继续等待。
            text = WebDriverWait(
                self.driver, timeout, poll_frequency=0.1,
                ignored_exceptions=(StaleElementReferenceException,),
            ).until(lambda driver: driver.find_element(*toast_loc).text)
        except TimeoutException:
            logger.info("未捕获到 Toast 提示")
            return ""
        logger.info(f"获取Toast提示:{text}")
        return text

    def base_get_shot(self,file_name):
        file_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', file_name)
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(BASE_DIR ,'img',f"{file_name}_{now}.jpg")
        self.driver.get_screenshot_as_file(file_path)

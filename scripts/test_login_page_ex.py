import pytest

from page.enter_home_page import EnterHomePage
from page.login_page import LoginPage
from base import logger
from utils.tools import read_json


@pytest.mark.parametrize(
    "username,passwd,expect,img",
    read_json('login_data.json', fields=('username', 'passwd', 'expect', 'img')),
)
class TestLoginPage:

    def test_login_page_parameter(self,first_app_driver,username,passwd,expect,img):
        EnterHomePage(first_app_driver).agree_eula()
        EnterHomePage(first_app_driver).skip_ad()
        login_page = LoginPage(first_app_driver)
        login_page.before_login()
        login_page.login(username,passwd)
        if img == "Login_Success" :
            result = login_page.base_get_text(login_page.login_success_loc)
        else:
            result = login_page.base_get_toast(login_page.login_fail_loc)
        logger.info(f"登录结果 : {result}")
        assert expect in result, f"登录结果不符合预期：{result}"
        login_page.base_get_shot(img)


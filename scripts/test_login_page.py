from page.enter_home_page import EnterHomePage
from page.login_page import LoginPage
from base import logger


class TestLoginPage:

    def test_login_page_success(self,first_app_driver):
        EnterHomePage(first_app_driver).agree_eula()
        EnterHomePage(first_app_driver).skip_ad()
        login_page = LoginPage(first_app_driver)
        login_page.before_login()
        login_page.login('17641160730','lzj123456!')
        result = login_page.base_get_text(login_page.login_success_loc)
        logger.info("登录结果：%s", result)
        assert result == '用户59907260', f"登录结果不符合预期：{result}"
        login_page.base_get_shot("Login_Successes")

    def test_login_page_fail(self,first_app_driver):
        EnterHomePage(first_app_driver).agree_eula()
        EnterHomePage(first_app_driver).skip_ad()
        login_page = LoginPage(first_app_driver)
        login_page.before_login()
        login_page.login('17641160730','lzj123456')
        result = login_page.base_get_toast(login_page.login_fail_loc)
        logger.info("登录结果：%s", result)
        assert result == '账号或密码不正确', f"登录结果不符合预期：{result}"
        login_page.base_get_shot("Login_Failed")

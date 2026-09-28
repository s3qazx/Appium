
from page.enter_home_page import EnterHomePage


class TestHomePage:

    def test_enter_home(self,first_app_driver):
        home = EnterHomePage(first_app_driver)
        home.agree_eula()
        home.skip_ad()
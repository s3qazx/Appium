"""无需设备的流程回归测试：python -m unittest test_flow_unit -v"""
import inspect
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from selenium.common.exceptions import (
    InvalidSessionIdException, StaleElementReferenceException,
    TimeoutException, WebDriverException,
)

import conftest as fixtures
from base.base_page import BasePage
from page.addcart_page import AddCartPage
from page.enter_home_page import EnterHomePage
from scripts import test_addcart_page as cart_test
from scripts import test_login_page as login_test
from scripts import test_login_page_ex as parameter_login_test
from utils import tools


class FlowTests(unittest.TestCase):
    def test_login_and_search_share_one_session(self):
        self.assertEqual(list(inspect.signature(fixtures.search_ok).parameters), ['login_ok', 'request'])
        driver = Mock()
        account = {'username': 'demo', 'passwd': 'demo', 'expect': '用户', 'img': 'Login_Success'}
        with patch.object(fixtures.webdriver, 'Remote', return_value=driver) as remote, \
             patch.object(fixtures, 'EnterHomePage'), patch.object(fixtures, 'AdPage'), \
             patch.object(fixtures, 'LoginPage') as login, \
             patch.object(fixtures, 'SearchPage') as search, \
             patch.object(fixtures.Path, 'open', mock_open(read_data=json.dumps([account]))):
            login.return_value.base_get_text.return_value = '用户 demo'
            lifecycle = fixtures.first_app_driver.__wrapped__()
            self.assertIs(next(lifecycle), driver)
            try:
                logged_in = fixtures.login_ok.__wrapped__(driver)
                ready = fixtures.search_ok.__wrapped__(logged_in, Mock(param='毛巾'))
                self.assertIs(ready, driver)
                remote.assert_called_once()
                search.assert_called_once_with(driver)
                search.return_value.search.assert_called_once_with('毛巾')
                driver.activate_app.assert_called_once()
                driver.quit.assert_not_called()
            finally:
                lifecycle.close()
            driver.quit.assert_called_once()

    def test_expired_session_does_not_break_cleanup(self):
        driver = Mock()
        driver.terminate_app.side_effect = InvalidSessionIdException('expired')
        driver.quit.side_effect = InvalidSessionIdException('expired')
        with patch.object(fixtures.webdriver, 'Remote', return_value=driver):
            lifecycle = fixtures._app_driver(fixtures.APP_CONFIG)
            next(lifecycle)
            lifecycle.close()
        driver.quit.assert_called_once()

    def test_other_cleanup_errors_are_not_hidden(self):
        driver = Mock()
        driver.terminate_app.side_effect = WebDriverException('transport failed')
        with patch.object(fixtures.webdriver, 'Remote', return_value=driver):
            lifecycle = fixtures._app_driver(fixtures.APP_CONFIG)
            next(lifecycle)
            with self.assertRaises(WebDriverException):
                lifecycle.close()
        driver.quit.assert_called_once()

    def test_optional_skip_timeout_but_not_click_error_is_ignored(self):
        page = EnterHomePage(Mock())
        with patch('page.enter_home_page.WebDriverWait') as wait:
            wait.return_value.until.side_effect = TimeoutException()
            self.assertFalse(page.skip_ad())
            wait.return_value.until.side_effect = None
            wait.return_value.until.return_value.click.side_effect = WebDriverException('click failed')
            with self.assertRaises(WebDriverException):
                page.skip_ad()

    def test_toast_retries_empty_and_stale_text(self):
        driver = Mock()
        driver.find_element.side_effect = [Mock(text=''), StaleElementReferenceException(), Mock(text='添加成功')]
        result = BasePage(driver).base_get_toast(('xpath', '//android.widget.Toast'), timeout=1)
        self.assertEqual(result, '添加成功')

    def test_toast_timeout_is_empty_but_invalid_session_propagates(self):
        driver = Mock()
        driver.find_element.return_value.text = ''
        page = BasePage(driver)
        self.assertEqual(page.base_get_toast(('xpath', '//android.widget.Toast'), timeout=0), '')
        driver.find_element.side_effect = InvalidSessionIdException('expired')
        with self.assertRaises(InvalidSessionIdException):
            page.base_get_toast(('xpath', '//android.widget.Toast'), timeout=0)

    def test_add_cart_reads_toast_immediately_after_confirmation(self):
        page = AddCartPage(Mock())
        actions = Mock()
        page.base_click = actions.click
        page.base_get_toast = actions.toast
        actions.toast.return_value = '添加成功'
        self.assertEqual(page.add_cart(), '添加成功')
        self.assertEqual([item[0] for item in actions.mock_calls], ['click', 'click', 'toast'])
        screenshot = page.driver.get_screenshot_as_file.call_args.args[0]
        self.assertTrue(Path(screenshot).name.startswith('添加购物车_添加成功_'))

    def test_missing_toast_is_an_explicit_failure(self):
        with patch.object(cart_test, 'AdPage'), patch.object(cart_test, 'AddCartPage') as cart:
            cart.return_value.add_cart.return_value = ''
            with self.assertRaisesRegex(AssertionError, '未捕获到加购 Toast'):
                cart_test.TestAddCartPage().test_add_cart_page(Mock())
            cart.return_value.back_to_home.assert_not_called()

    def test_add_cart_preserves_missing_toast(self):
        page = AddCartPage(Mock())
        page.base_click = Mock()
        page.base_get_toast = Mock(return_value='')
        page.base_get_shot = Mock()
        self.assertEqual(page.add_cart(), '')
        page.base_get_shot.assert_called_once_with('添加购物车_未捕获Toast')

    def test_screenshot_filename_preserves_text_and_replaces_invalid_characters(self):
        driver = Mock()
        BasePage(driver).base_get_shot('添加购物车_失败:库存/不足?')
        screenshot = driver.get_screenshot_as_file.call_args.args[0]
        self.assertTrue(Path(screenshot).name.startswith('添加购物车_失败_库存_不足__'))

    def test_failed_login_reads_toast_once(self):
        with patch.object(login_test, 'EnterHomePage'), patch.object(login_test, 'LoginPage') as login:
            login.return_value.base_get_toast.side_effect = ['账号或密码不正确', '']
            login_test.TestLoginPage().test_login_page_fail(Mock())
            login.return_value.base_get_toast.assert_called_once()

    def test_parameterized_failed_login_checks_toast(self):
        with patch.object(parameter_login_test, 'EnterHomePage'), \
             patch.object(parameter_login_test, 'LoginPage') as login:
            login.return_value.base_get_toast.return_value = '账号或密码不正确'
            parameter_login_test.TestLoginPage().test_login_page_parameter(
                Mock(), 'demo', 'wrong', '账号或密码不正确', 'Login_Failed',
            )
            login.return_value.base_get_text.assert_not_called()

    def test_json_fields_do_not_depend_on_key_order(self):
        row = {'img': 'Login_Success', 'expect': '用户', 'passwd': 'demo', 'username': 'demo-user'}
        with patch.object(Path, 'open', mock_open(read_data=json.dumps([row]))):
            self.assertEqual(
                tools.read_json('login_data.json', fields=('username', 'passwd', 'expect', 'img')),
                [('demo-user', 'demo', '用户', 'Login_Success')],
            )
        with patch.object(Path, 'open', mock_open(read_data='["keyword"]')):
            self.assertEqual(tools.read_json('search_keyword.json'), ['keyword'])

    def test_logger_creates_directory_and_reuses_handler(self):
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(tools, 'BASE_DIR', directory), \
             patch.object(tools.GetLog, '_GetLog__log', None), \
             patch.object(tools.logging, 'getLogger', return_value=Mock()) as get_logger:
            logger = tools.GetLog.get_log()
            handler = logger.addHandler.call_args.args[0]
            try:
                self.assertTrue((Path(directory) / 'log' / 'automation.log').is_file())
                self.assertIs(tools.GetLog.get_log(), logger)
                get_logger.assert_called_once_with('appautomation')
                logger.addHandler.assert_called_once()
            finally:
                handler.close()


if __name__ == '__main__':
    unittest.main()

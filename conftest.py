import json
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import InvalidSessionIdException

from base import logger
from config import APPIUM_SEVER, APP_CONFIG, BASE_DIR, DEVICE_CONFIG, First_APP_CONFIG
from page.ad_page import AdPage
from page.enter_home_page import EnterHomePage
from page.login_page import LoginPage
from page.search_page import SearchPage
from utils.tools import read_json


def _app_driver(app_config):
    caps = {**DEVICE_CONFIG, **app_config}
    option = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote(APPIUM_SEVER, options=option)
    try:
        yield driver
    finally:
        try:
            driver.terminate_app(caps['appPackage'])
        except InvalidSessionIdException:
            logger.warning("清理时会话已失效，无法关闭 App")
        finally:
            try:
                driver.quit()
            except InvalidSessionIdException:
                logger.warning("清理时会话已结束，无需重复退出")


@pytest.fixture
def first_app_driver():
    yield from _app_driver(First_APP_CONFIG)


@pytest.fixture
def app_driver():
    yield from _app_driver(APP_CONFIG)


@pytest.fixture
def login_ok(first_app_driver):
    # 从现有数据中选择成功登录账号，不在 fixture 中重复写账号密码。
    with (Path(BASE_DIR) / "data" / "login_data.json").open(encoding="utf-8") as file:
        rows = json.load(file)
    account = next((row for row in rows if row.get("img") == "Login_Success"), None)
    if account is None:
        raise ValueError("login_data.json 缺少 img=Login_Success 的登录数据")

    home = EnterHomePage(first_app_driver)
    home.agree_eula()
    home.skip_ad()
    ad = AdPage(first_app_driver)
    ad.remove_add(ad.remove_add_button_loc)
    login = LoginPage(first_app_driver)
    login.before_login()
    login.login(account["username"], account["passwd"])
    assert account["expect"] in login.base_get_text(login.login_success_loc), "登录结果不符合预期"

    # 保留原来的重新打开 App 流程，但复用当前会话。
    first_app_driver.terminate_app(First_APP_CONFIG['appPackage'])
    first_app_driver.activate_app(First_APP_CONFIG['appPackage'])
    home.skip_ad()
    ad.remove_add(ad.remove_add_button_loc)
    return first_app_driver


@pytest.fixture(params=read_json("search_keyword.json"))
def search_ok(login_ok, request):
    search = SearchPage(login_ok)
    search.search(request.param)
    search.fd_element(search.first_result_loc)
    return login_ok

import pytest

from page.enter_home_page import EnterHomePage
from page.search_page import SearchPage
from utils.tools import read_json
from base import logger


@pytest.mark.parametrize("keyword",read_json('search_keyword.json'))
class TestSearchPage:

    def test_search_success(self,app_driver,keyword):
        EnterHomePage(app_driver).skip_ad()
        search_page = SearchPage(app_driver)
        search_page.search(keyword)
        result = search_page.base_get_text(search_page.first_result_loc)
        logger.info(f"第一个搜索结果:{result}")
        assert keyword in result,''
        search_page.base_get_shot(f"search-{keyword} result")
from page.ad_page import AdPage
from page.addcart_page import AddCartPage
from base import logger


class TestAddCartPage:
    def test_add_cart_page(self, search_ok):
        ad = AdPage(search_ok)
        ad.remove_add(ad.remove_add_button_loc)
        cart = AddCartPage(search_ok)
        cart.enter_goods_details()
        result = cart.add_cart()
        logger.info("添加购物车提示：%s", result or "未捕获到提示")
        assert result, "未捕获到加购 Toast，无法据此判断商品是否已加入购物车"
        assert "成功" in result, f"加购提示不符合预期：{result}"
        cart.back_to_home()

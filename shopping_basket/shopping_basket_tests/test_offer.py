import pytest
from offer import Offer, BuyXgetY, PercentDiscount, BuyNofXGetCheapestForFree
from basket import Basket
from catalogue import Catalogue


@pytest.fixture
def buy_x_get_y():
    return BuyXgetY("item", 3, 2)


@pytest.fixture
def percent_discount():
    return PercentDiscount("item", 20)


@pytest.fixture
def cheapest_for_free_offer():
    return BuyNofXGetCheapestForFree({"item1", "item2"}, 5)


def testOffer_is_applicable():
    with pytest.raises(NotImplementedError):
        Offer().is_applicable(Basket({}))


def testOffer_select_items():
    with pytest.raises(NotImplementedError):
        Offer().select_items(Basket({}))


def testOffer_products_per_offer():
    assert Offer().products_per_offer() == None


def testOffer_calculate_discount():
    with pytest.raises(NotImplementedError):
        Offer().calculate_discount(Basket({}), Catalogue({}))


def testBuyXgetY_is_applicable_1(buy_x_get_y):
    assert buy_x_get_y.is_applicable(Basket({})) == False


def testBuyXgetY_is_applicable_2(buy_x_get_y):
    assert buy_x_get_y.is_applicable(Basket({"otheritem": 5})) == False


def testBuyXgetY_is_applicable_3(buy_x_get_y):
    assert buy_x_get_y.is_applicable(Basket({"item": 2})) == False


def testBuyXgetY_is_applicable_4(buy_x_get_y):
    assert buy_x_get_y.is_applicable(Basket({"otheritem": 4, "item": 3})) == False


def testBuyXgetY_is_applicable_5(buy_x_get_y):
    assert buy_x_get_y.is_applicable(Basket({"item": 4})) == True


def testBuyXgetY_select_items(buy_x_get_y):
    assert buy_x_get_y.select_items(Basket({"item": 10})) == Basket({"item": 5})


def testBuyXgetY_products_per_offer(buy_x_get_y):
    assert buy_x_get_y.products_per_offer() == None


def testBuyXgetY_calculate_discount(buy_x_get_y):
    basket = Basket({"item": 5})
    catalogue = Catalogue({"item": 2})
    assert buy_x_get_y.calculate_discount(basket, catalogue) == 4


def testPercentDiscount_is_applicable_1(percent_discount):
    assert percent_discount.is_applicable(Basket({})) == False


def testPercentDiscount_is_applicable_2(percent_discount):
    assert percent_discount.is_applicable(Basket({"otheritem": 5})) == False


def testPercentDiscount_is_applicable_3(percent_discount):
    assert percent_discount.is_applicable(Basket({"item": 1})) == True


def testPercentDiscount_is_applicable_4(percent_discount):
    assert percent_discount.is_applicable(Basket({"item": 2})) == True


def testPercentDiscount_select_items(percent_discount):
    assert percent_discount.select_items(Basket({"item": 10})) == Basket({"item": 1})


def testPercentDiscount_products_per_offer(percent_discount):
    assert percent_discount.products_per_offer() == None


def testPercentDiscount_calculate_discount(percent_discount):
    basket = Basket({"item": 1})
    catalogue = Catalogue({"item": 10})
    assert percent_discount.calculate_discount(basket, catalogue) == 2


def testBuyNofXGetCheapestForFree_is_applicable_1(cheapest_for_free_offer):
    assert cheapest_for_free_offer.is_applicable(Basket({})) == False


def testBuyNofXGetCheapestForFree_is_applicable_2(cheapest_for_free_offer):
    assert cheapest_for_free_offer.is_applicable(Basket({"item1": 4})) == False


def testBuyNofXGetCheapestForFree_is_applicable_3(cheapest_for_free_offer):
    assert cheapest_for_free_offer.is_applicable(Basket({"item2": 4})) == False


def testBuyNofXGetCheapestForFree_is_applicable_4(cheapest_for_free_offer):
    assert cheapest_for_free_offer.is_applicable(Basket({"item1": 5})) == True


def testBuyNofXGetCheapestForFree_is_applicable_5(cheapest_for_free_offer):
    assert cheapest_for_free_offer.is_applicable(Basket({"item2": 5})) == True


def testBuyNofXGetCheapestForFree_is_applicable_6(cheapest_for_free_offer):
    basket = Basket({"item1": 4, "item2": 1})
    assert cheapest_for_free_offer.is_applicable(basket) == True


def testBuyNofXGetCheapestForFree_is_applicable_7(cheapest_for_free_offer):
    basket = Basket({"item1": 4, "item2": 2})
    assert cheapest_for_free_offer.is_applicable(basket) == True


def testBuyNofXGetCheapestForFree_select_items(cheapest_for_free_offer):
    basket_in = Basket({"item1": 4, "item2": 2})
    basket_out = Basket({"item1": 5, "item2": 5})
    assert cheapest_for_free_offer.select_items(basket_in) == basket_out


def testBuyNofXGetCheapestForFree_products_per_offer(cheapest_for_free_offer):
    assert cheapest_for_free_offer.products_per_offer() == 5


def testBuyNofXGetCheapestForFree_calculate_discount_1(cheapest_for_free_offer):
    basket = Basket({"item1": 4, "item2": 1})
    catalogue = Catalogue({"item1": 10, "item2": 20})
    assert cheapest_for_free_offer.calculate_discount(basket, catalogue) == 10


def testBuyNofXGetCheapestForFree_calculate_discount_2(cheapest_for_free_offer):
    basket = Basket({"item1": 4, "item2": 1})
    catalogue = Catalogue({"item1": 20, "item2": 5})
    assert cheapest_for_free_offer.calculate_discount(basket, catalogue) == 5

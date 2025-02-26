import pytest
from offer import Offer, BuyXgetY, PercentDiscount, BuyNofXGetCheapestForFree
from basket import Basket
from catalogue import Catalogue
from basket_pricer import basket_pricer


class Broken1(Offer):
    def is_applicable(self, basket):
        return True

    def select_items(self, basket):
        return basket

    def calculate_discount(self, offer_items, prices):
        return 0


class Broken2(Offer):
    def is_applicable(self, basket):
        return True

    def select_items(self, basket):
        return basket

    def calculate_discount(self, offer_items, prices):
        return 999


class Broken3(Offer):
    def is_applicable(self, basket):
        return True

    def select_items(self, basket):
        return basket

    def calculate_discount(self, offer_items, prices):
        return -999


@pytest.fixture
def catalogue():
    return Catalogue(
        {
            "Baked Beans": 0.99,
            "Biscuits": 1.20,
            "Sardines": 1.89,
            "Shampoo (Small)": 2.00,
            "Shampoo (Medium)": 2.50,
            "Shampoo (Large)": 3.50,
        }
    )


@pytest.fixture
def offers():
    return [
        BuyXgetY("Baked Beans", 2, 1),
        PercentDiscount("Sardines", 25),
        BuyNofXGetCheapestForFree(
            {"Shampoo (Large)", "Shampoo (Medium)", "Shampoo (Small)"}, 3
        ),
    ]


def testBuyXgetY(catalogue, offers):
    basket = Basket({"Baked Beans": 4, "Biscuits": 1})
    assert basket_pricer(basket, catalogue, offers) == (5.16, 0.99, 4.17)


def testBuyXgetYtwice(catalogue, offers):
    basket = Basket({"Baked Beans": 6})
    assert basket_pricer(basket, catalogue, offers) == (5.94, 1.98, 3.96)


def testPercentDiscount(catalogue, offers):
    basket = Basket({"Baked Beans": 2, "Biscuits": 1, "Sardines": 2})
    assert basket_pricer(basket, catalogue, offers) == (6.96, 0.95, 6.01)


def testBuyNofXGetCheapestForFree(catalogue, offers):
    basket = Basket({"Shampoo (Large)": 3, "Shampoo (Medium)": 1, "Shampoo (Small)": 2})
    assert basket_pricer(basket, catalogue, offers) == (17.0, 5.5, 11.5)


def testBrokenOffersZeroDiscount(catalogue):
    basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
    assert basket_pricer(basket, catalogue, [Broken1()]) == (9.06, 0.0, 9.06)


def testBrokenOfferDiscountTooLarge(catalogue):
    basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
    with pytest.raises(ValueError):
        basket_pricer(basket, catalogue, [Broken2()])


def testBrokenOfferNegativeDiscount(catalogue):
    basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
    with pytest.raises(ValueError):
        basket_pricer(basket, catalogue, [Broken3()])


def testEmptyCatalogue():
    basket = Basket({"item": 1})
    with pytest.raises(ValueError):
        basket_pricer(basket, Catalogue({}), [Broken3()])


def testNegativePrice():
    basket = Basket({"item": 1})
    with pytest.raises(ValueError):
        basket_pricer(basket, Catalogue({"item": -1}), [Broken3()])


def testItemNotInCatalogue(catalogue, offers):
    basket = Basket({"qwerty": 1})
    with pytest.raises(ValueError):
        basket_pricer(basket, catalogue, offers)


def testEmptyBasket(catalogue, offers):
    assert basket_pricer(Basket(), catalogue, offers) == (0.0, 0.0, 0.0)

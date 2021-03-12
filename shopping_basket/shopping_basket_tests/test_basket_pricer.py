import unittest
from offer import Offer, BuyXgetY, PercentDiscount, BuyNofXGetCheapestForFree
from basket import Basket
from catalogue import Catalogue
from basket_pricer import basket_pricer

catalogue = Catalogue(
    {
        "Baked Beans": 0.99,
        "Biscuits": 1.20,
        "Sardines": 1.89,
        "Shampoo (Small)": 2.00,
        "Shampoo (Medium)": 2.50,
        "Shampoo (Large)": 3.50,
    }
)

offers = [
    BuyXgetY("Baked Beans", 2, 1),
    PercentDiscount("Sardines", 25),
    BuyNofXGetCheapestForFree(
        {"Shampoo (Large)", "Shampoo (Medium)", "Shampoo (Small)"}, 3
    ),
]


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


class TestBasketPricer(unittest.TestCase):
    def testBuyXgetY(self):
        basket = Basket({"Baked Beans": 4, "Biscuits": 1})
        self.assertEqual(basket_pricer(basket, catalogue, offers), (5.16, 0.99, 4.17))

    def testBuyXgetYtwice(self):
        basket = Basket({"Baked Beans": 6})
        self.assertEqual(basket_pricer(basket, catalogue, offers), (5.94, 1.98, 3.96))

    def testPercentDiscount(self):
        basket = Basket({"Baked Beans": 2, "Biscuits": 1, "Sardines": 2})
        self.assertEqual(basket_pricer(basket, catalogue, offers), (6.96, 0.95, 6.01))

    def testBuyNofXGetCheapestForFree(self):
        basket = Basket(
            {"Shampoo (Large)": 3, "Shampoo (Medium)": 1, "Shampoo (Small)": 2}
        )
        self.assertEqual(basket_pricer(basket, catalogue, offers), (17.0, 5.5, 11.5))

    def testBrokenOffersZeroDiscount(self):
        basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
        self.assertEqual(
            basket_pricer(basket, catalogue, [Broken1()]), (9.06, 0.0, 9.06)
        )

    def testBrokenOfferDiscountTooLarge(self):
        basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
        with self.assertRaises(ValueError):
            basket_pricer(basket, catalogue, [Broken2()])

    def testBrokenOfferNegativeDiscount(self):
        basket = Basket({"Baked Beans": 1, "Biscuits": 2, "Sardines": 3})
        with self.assertRaises(ValueError):
            basket_pricer(basket, catalogue, [Broken3()])

    def testEmptyCatalogue(self):
        basket = Basket({"item": 1})
        with self.assertRaises(ValueError):
            basket_pricer(basket, Catalogue({}), [Broken3()])

    def testNegativePrice(self):
        basket = Basket({"item": 1})
        with self.assertRaises(ValueError):
            basket_pricer(basket, Catalogue({"item": -1}), [Broken3()])

    def testItemNotInCatalogue(self):
        basket = Basket({"qwerty": 1})
        with self.assertRaises(ValueError):
            basket_pricer(basket, catalogue, offers)

    def testEmptyBasket(self):
        self.assertEqual(basket_pricer(Basket(), catalogue, offers), (0.0, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()

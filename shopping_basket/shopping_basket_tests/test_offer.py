import unittest
from offer import Offer, BuyXgetY, PercentDiscount, BuyNofXGetCheapestForFree
from basket import Basket
from catalogue import Catalogue


class TestOffer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.buy_x_get_y = BuyXgetY("item", 3, 2)
        self.percent_discount = PercentDiscount("item", 20)
        self.cheapest_for_free_offer = BuyNofXGetCheapestForFree({"item1", "item2"}, 5)
        super().__init__(*args, **kwargs)

    def testOffer_is_applicable(self):
        with self.assertRaises(NotImplementedError):
            Offer().is_applicable(Basket({}))

    def testOffer_select_items(self):
        with self.assertRaises(NotImplementedError):
            Offer().select_items(Basket({}))

    def testOffer_products_per_offer(self):
        self.assertEqual(Offer().products_per_offer(), None)

    def testOffer_calculate_discount(self):
        with self.assertRaises(NotImplementedError):
            Offer().calculate_discount(Basket({}), Catalogue({}))

    def testBuyXgetY_is_applicable_1(self):
        self.assertEqual(self.buy_x_get_y.is_applicable(Basket({})), False)

    def testBuyXgetY_is_applicable_2(self):
        self.assertEqual(
            self.buy_x_get_y.is_applicable(Basket({"otheritem": 5})), False
        )

    def testBuyXgetY_is_applicable_3(self):
        self.assertEqual(self.buy_x_get_y.is_applicable(Basket({"item": 2})), False)

    def testBuyXgetY_is_applicable_4(self):
        self.assertEqual(
            self.buy_x_get_y.is_applicable(Basket({"otheritem": 4, "item": 3})), False
        )

    def testBuyXgetY_is_applicable_5(self):
        self.assertEqual(self.buy_x_get_y.is_applicable(Basket({"item": 4})), True)

    def testBuyXgetY_select_items(self):
        self.assertEqual(
            self.buy_x_get_y.select_items(Basket({"item": 10})), Basket({"item": 5})
        )

    def testBuyXgetY_products_per_offer(self):
        self.assertEqual(self.buy_x_get_y.products_per_offer(), None)

    def testBuyXgetY_calculate_discount(self):
        self.assertEqual(
            self.buy_x_get_y.calculate_discount(
                Basket({"item": 5}), Catalogue({"item": 2})
            ),
            4,
        )

    def testPercentDiscount_is_applicable_1(self):
        self.assertEqual(self.percent_discount.is_applicable(Basket({})), False)

    def testPercentDiscount_is_applicable_2(self):
        self.assertEqual(
            self.percent_discount.is_applicable(Basket({"otheritem": 5})), False
        )

    def testPercentDiscount_is_applicable_3(self):
        self.assertEqual(self.percent_discount.is_applicable(Basket({"item": 1})), True)

    def testPercentDiscount_is_applicable_4(self):
        self.assertEqual(self.percent_discount.is_applicable(Basket({"item": 2})), True)

    def testPercentDiscount_select_items(self):
        self.assertEqual(
            self.percent_discount.select_items(Basket({"item": 10})),
            Basket({"item": 1}),
        )

    def testPercentDiscount_products_per_offer(self):
        self.assertEqual(self.percent_discount.products_per_offer(), None)

    def testPercentDiscount_calculate_discount(self):
        self.assertEqual(
            self.percent_discount.calculate_discount(
                Basket({"item": 1}), Catalogue({"item": 10})
            ),
            2,
        )

    def testBuyNofXGetCheapestForFree_is_applicable_1(self):
        self.assertEqual(self.cheapest_for_free_offer.is_applicable(Basket({})), False)

    def testBuyNofXGetCheapestForFree_is_applicable_2(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(Basket({"item1": 4})), False
        )

    def testBuyNofXGetCheapestForFree_is_applicable_3(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(Basket({"item2": 4})), False
        )

    def testBuyNofXGetCheapestForFree_is_applicable_4(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(Basket({"item1": 5})), True
        )

    def testBuyNofXGetCheapestForFree_is_applicable_5(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(Basket({"item2": 5})), True
        )

    def testBuyNofXGetCheapestForFree_is_applicable_6(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(
                Basket({"item1": 4, "item2": 1})
            ),
            True,
        )

    def testBuyNofXGetCheapestForFree_is_applicable_7(self):
        self.assertEqual(
            self.cheapest_for_free_offer.is_applicable(
                Basket({"item1": 4, "item2": 2})
            ),
            True,
        )

    def testBuyNofXGetCheapestForFree_select_items(self):
        self.assertEqual(
            self.cheapest_for_free_offer.select_items(Basket({"item1": 4, "item2": 2})),
            Basket({"item1": 5, "item2": 5}),
        )

    def testBuyNofXGetCheapestForFree_products_per_offer(self):
        self.assertEqual(self.cheapest_for_free_offer.products_per_offer(), 5)

    def testBuyNofXGetCheapestForFree_calculate_discount_1(self):
        self.assertEqual(
            self.cheapest_for_free_offer.calculate_discount(
                Basket({"item1": 4, "item2": 1}), Catalogue({"item1": 10, "item2": 20})
            ),
            10,
        )

    def testBuyNofXGetCheapestForFree_calculate_discount_2(self):
        self.assertEqual(
            self.cheapest_for_free_offer.calculate_discount(
                Basket({"item1": 4, "item2": 1}), Catalogue({"item1": 20, "item2": 5})
            ),
            5,
        )


if __name__ == "__main__":
    unittest.main()

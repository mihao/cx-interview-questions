from basket import Basket
from catalogue import Catalogue


class Offer:
    # Should return True if the offer is applicable for the given basket, False
    # otherwise.
    def is_applicable(self, basket: Basket) -> bool:
        raise NotImplementedError

    # Should return a Basket with the items covered by the offer. Any elements
    # that are not in the customer's basket will be ignored. The customer's
    # basket is passed as an argument.
    def select_items(self, basket: Basket) -> Basket:
        raise NotImplementedError

    # If the returned value is an int, it is the maximal number of products that
    # can be covered by the offer. If the intersection of select_items() with
    # the customer's basket has more than n elements, only n most expensive ones
    # will be used (where n is the value returned by products_per_offer()). By
    # default products_per_offer() returns None, which means that there is no
    # limit.
    def products_per_offer(self) -> int:
        return None

    # Given a Basket of items covered by the offer and a Catalogue of prices,
    # calculate the value of the discount.
    def calculate_discount(self, offer_items: Basket, prices: Catalogue) -> float:
        raise NotImplementedError


class BuyXgetY(Offer):
    def __init__(self, item: str, buy_cnt: int, get_cnt: int):
        self.item = item
        self.buy_cnt = buy_cnt
        self.get_cnt = get_cnt

    def is_applicable(self, basket: Basket) -> bool:
        return basket[self.item] >= self.buy_cnt

    def select_items(self, basket: Basket) -> Basket:
        return Basket({self.item: self.buy_cnt + self.get_cnt})

    def calculate_discount(self, offer_items: Basket, prices: Catalogue) -> float:
        return prices[self.item] * (offer_items[self.item] - self.buy_cnt)


class PercentDiscount(Offer):
    def __init__(self, item: str, percent_discount: float):
        self.item = item
        self.percent_discount = percent_discount

    def is_applicable(self, basket: Basket) -> bool:
        return basket[self.item] >= 1

    def select_items(self, basket: Basket) -> Basket:
        return Basket({self.item: 1})

    def calculate_discount(self, offer_items: Basket, prices: Catalogue) -> float:
        return prices[self.item] * self.percent_discount / 100


class BuyNofXGetCheapestForFree(Offer):
    def __init__(self, items: set, n: int):
        self.n = n
        self.items = Basket({item: self.n for item in set(items)})

    def is_applicable(self, basket: Basket) -> bool:
        return sum((basket & self.items).values()) >= self.n

    def select_items(self, basket: Basket) -> Basket:
        return self.items

    def products_per_offer(self) -> int:
        return self.n

    def calculate_discount(self, offer_items: Basket, prices: Catalogue) -> float:
        return min(prices[item] for item in offer_items)

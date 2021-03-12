from decimal import Decimal, ROUND_HALF_UP
from typing import List
from offer import Offer
from basket import Basket
from catalogue import Catalogue


def round_half_up(num, precision=2):
    return float(
        (Decimal(str(num)) * Decimal(10) ** precision).quantize(1, ROUND_HALF_UP)
        / Decimal(10) ** precision
    )


def basket_pricer(basket: Basket, prices: Catalogue, offers: List[Offer]):
    def get_discount_and_offer_items(current_basket: Basket, offer: Offer):
        if not offer.is_applicable(current_basket):
            return None
        offer_items = current_basket & offer.select_items(current_basket)
        if not offer_items:
            return None
        products_per_offer = offer.products_per_offer()
        if products_per_offer is not None:
            sorted_items = sorted(
                offer_items.elements(), key=lambda item: prices[item], reverse=True
            )
            offer_items = Basket(sorted_items[:products_per_offer])
        discount = offer.calculate_discount(offer_items, prices)
        if discount > sum(prices[item] for item in offer_items.elements()):
            raise ValueError("discount is larger than the value of the items")
        return (discount, offer_items)

    try:
        sub_total = sum(prices[item] for item in basket.elements())
    except KeyError as e:
        raise ValueError(f"basket item not found in the catalogue: {e}") from None
    discount = 0.0
    undiscounted_basket_items = basket.copy()
    while True:
        offer_tuples = (
            get_discount_and_offer_items(undiscounted_basket_items, offer)
            for offer in offers
        )
        nonempty_offer_tuples = list(filter(None, offer_tuples))
        if not nonempty_offer_tuples:
            break
        best_discount, best_offer_items = max(nonempty_offer_tuples, key=lambda x: x[0])
        if not best_offer_items:
            break
        while undiscounted_basket_items & best_offer_items == best_offer_items:
            discount += best_discount
            undiscounted_basket_items -= best_offer_items

    sub_total_rounded = round_half_up(sub_total)
    discount_rounded = round_half_up(discount)
    return sub_total_rounded, discount_rounded, round_half_up(sub_total_rounded - discount_rounded)

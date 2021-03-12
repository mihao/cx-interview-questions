from decimal import Decimal, ROUND_HALF_UP
from typing import List
from offer import Offer
from basket import Basket
from catalogue import Catalogue


def _round_half_up(num, precision=2):
    return float(
        (Decimal(str(num)) * Decimal(10) ** precision).quantize(1, ROUND_HALF_UP)
        / Decimal(10) ** precision
    )


def _get_discount_and_offer_items(
    current_basket: Basket, offer: Offer, prices: Catalogue
):
    """
    Given a Basket and an Offer, the function returns None when the offer
    is not applicable to the given basket, and otherwise returns a tuple
    (discount, offer_items), where the first element is a float with the value
    of the calculated discount, and the second element is a Basket of products
    applicable to the discount.
    """

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
    if discount < 0:
        raise ValueError("discount cannot be negative")
    if discount > sum(prices[item] for item in offer_items.elements()):
        raise ValueError("discount cannot be larger than the value of the items")
    return (discount, offer_items)


def _calculate_discount_for_basket(
    basket: Basket, offers: List[Offer], prices: Catalogue
):
    """
    Main loop of the pricer algorithm. It starts with a temporary copy of the
    whole basket, finds an offer that gives the biggest discount for the
    given basket, and applies it as many times as possible, removing it from
    the temporary basket. Then the whole process is repeated, until there is
    no discount that can be applied to the remaining temporary basket.
    """

    discount = 0.0
    undiscounted_basket_items = basket.copy()
    while True:
        offer_tuples = (
            _get_discount_and_offer_items(undiscounted_basket_items, offer, prices)
            for offer in offers
        )
        nonempty_offer_tuples = list(filter(None, offer_tuples))
        if not nonempty_offer_tuples:
            break
        best_discount, best_offer_items = max(nonempty_offer_tuples, key=lambda x: x[0])
        if not best_offer_items:
            break
        discount_cnt = 0
        while undiscounted_basket_items & best_offer_items == best_offer_items:
            discount_cnt += 1
            undiscounted_basket_items -= best_offer_items
        discount += discount_cnt * best_discount
    return discount


def basket_pricer(basket: Basket, prices: Catalogue, offers: List[Offer]):
    """
    Function for invoking the basket pricer.

    Arguments:
    basket: a Counter-like structure with item names as keys, and their quantity as the value
    prices: a dict-like structure with item names as keys, and their prices as the value
    offers: list of offers (subclasses of Offer, which is an abstract class)
    Returned value:
    tuple containing three floats: sub-total, discount and the total discounted price
    """

    if any(value < 0 for value in prices.values()):
        raise ValueError("catalogue prices cannot be negative")

    try:
        sub_total = sum(prices[item] for item in basket.elements())
    except KeyError as e:
        raise ValueError(f"basket item not found in the catalogue: {e}") from None

    sub_total_rounded = _round_half_up(sub_total)
    discount = _calculate_discount_for_basket(basket, offers, prices)
    discount_rounded = _round_half_up(discount)
    return (
        sub_total_rounded,
        discount_rounded,
        _round_half_up(sub_total_rounded - discount_rounded),
    )

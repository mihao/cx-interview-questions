## Basket pricer

To use the basket pricer, first import relevant classes and functions:

    from offer import Offer, BuyXgetY, PercentDiscount, BuyNofXGetCheapestForFree
    from basket import Basket
    from catalogue import Catalogue
    from basket_pricer import basket_pricer

Create a catalogue (which maps item names to their prices):

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

Create a basket:

    basket = Basket({"Baked Beans": 4, "Biscuits": 1})

Create a list of offers:

    offers = [
        BuyXgetY("Baked Beans", 2, 1),
        PercentDiscount("Sardines", 25),
        BuyNofXGetCheapestForFree(
            {"Shampoo (Large)", "Shampoo (Medium)", "Shampoo (Small)"}, 3
        ),
    ]

You can use predefined offer creators (`BuyXgetY`, `PercentDiscount`,
`BuyNofXGetCheapestForFree`) or create your own one by subclassing `Offer`.
Details on the interface exposed by `Offer` are in `offer.py`.

Finally, call the basket pricer:

    sub_total, discount, total = basket_pricer(basket, catalogue, offers)
    # Should return (5.16, 0.99, 4.17)

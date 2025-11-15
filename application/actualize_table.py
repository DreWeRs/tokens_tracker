from application.get_actual_table import get_actual_table
from application.get_crypto_currency import (
    CryptoCurrencyGetter,
    get_desired_currencies_price,
)
from application.get_desired_currencies import get_desired_currencies


def actualize_table(previous_table: list[list], crypto_getter: CryptoCurrencyGetter):
    data = crypto_getter.get_currencies()
    desired_currency = get_desired_currencies(previous_table)
    prices = get_desired_currencies_price(data, desired_currency)
    actual_table = get_actual_table(prices, previous_table)
    return actual_table

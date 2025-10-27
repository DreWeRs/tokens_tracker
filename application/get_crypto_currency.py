from typing import Any

from requests import request


class CryptoCurrencyGetter:
    def __init__(self, url: str):
        self.url = url

    def get_currencies(self) -> list[dict[str, Any]]:
        response = request(url=self.url, method='get')
        status = response.status_code

        if status != 200:
            raise ValueError('Проверьте подключение к интернету')

        data = response.json()

        if not data:
            raise ValueError('Ошибка доступа к онлайн-сервисам')

        return data['get']


def get_desired_currencies_price(
        data: list[dict[str, Any]],
        desired_currencies: list[str]
) -> dict[str, int]:
    currency_prices = {}

    for elem in data:
        crypto_symbol = elem['symbol']
        if crypto_symbol in desired_currencies:
            currency_prices[crypto_symbol] = int(elem['price_usd'])

    return currency_prices

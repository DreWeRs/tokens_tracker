from typing import Any

from requests import request


class CryptoCurrencyGetter:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_currencies(self) -> list[dict[str, Any]]:
        response = request(url=self.url, method="get", timeout=10.0)
        status = response.status_code

        if status != 200:
            raise ValueError("Проверьте подключение к интернету")

        data = response.json()["data"]

        if not data:
            raise AttributeError("Ошибка доступа к онлайн-сервисам")

        return data

    def get_currencies_names(self, data: list[dict[str: Any]]) -> list[str]:
        currency_names = [elem["symbol"] for elem in data]
        return currency_names


def get_desired_currencies_price(
        data: list[dict[str, Any]],
        desired_currencies: list[str],
) -> dict[str, float]:
    currency_prices = {}

    for elem in data:
        crypto_symbol = elem["symbol"]
        if crypto_symbol in desired_currencies:
            currency_prices[crypto_symbol] = float(elem["price_usd"])

    return currency_prices

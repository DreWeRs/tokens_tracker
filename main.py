import sys

from PyQt6.QtWidgets import QApplication

from application.get_actual_table import get_actual_table
from application.get_crypto_currency import (
    CryptoCurrencyGetter,
    get_desired_currencies_price,
)
from application.get_desired_currencies import get_desired_currencies
from config import load_config
from presentation.main_window import MainWindow


def main() -> None:
    config = load_config()
    crypto_getter = CryptoCurrencyGetter(config.url)

    data = crypto_getter.get_currencies()

    table = [
        ["BTC", "19000", "0", "19000", "27.10.2025"],
        ["TON", "5.90", "0", "0", "10.10.2025"],
    ]  # Just for test, it will be implemented through database later

    desired_currency = get_desired_currencies(table)
    prices = get_desired_currencies_price(data, desired_currency)
    actual_table = get_actual_table(prices, table)

    app = QApplication(sys.argv)
    ex = MainWindow(actual_table)
    ex.fill_table()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

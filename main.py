import sys

from PyQt6.QtWidgets import QApplication

from application.get_actual_table import get_actual_table
from application.get_crypto_currency import (
    CryptoCurrencyGetter,
    get_desired_currencies_price,
)
from application.get_desired_currencies import get_desired_currencies
from config import load_config
from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository
from presentation.main_window import MainWindow


def main() -> None:
    config = load_config()
    session_maker = SQLiteSessionMaker(config)
    crypto_getter = CryptoCurrencyGetter(config.url)

    connection = session_maker.create_connection()
    cur = connection.cursor()
    table = CryptoCurrencyRepository(cur).read_currencies_table()
    table = [list(elem)[1:] for elem in table]

    data = crypto_getter.get_currencies()
    desired_currency = get_desired_currencies(table)
    prices = get_desired_currencies_price(data, desired_currency)
    actual_table = get_actual_table(prices, table)

    app = QApplication(sys.argv)
    ex = MainWindow(actual_table, session_maker)
    ex.fill_table()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

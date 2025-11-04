import sys

from PyQt6.QtWidgets import QApplication

from application.get_crypto_currency import CryptoCurrencyGetter
from config import load_config
from infrastructure.db.db_setup import SQLiteSessionMaker
from presentation.main_window import MainWindow


def main() -> None:
    config = load_config()
    session_maker = SQLiteSessionMaker(config)
    crypto_getter = CryptoCurrencyGetter(config.url)

    app = QApplication(sys.argv)
    ex = MainWindow(session_maker, crypto_getter)
    ex.fill_table()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

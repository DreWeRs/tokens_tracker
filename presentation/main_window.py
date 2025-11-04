from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from application.actualize_table import actualize_table
from application.get_crypto_currency import CryptoCurrencyGetter, get_desired_currencies_price
from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository
from presentation.add_token_window import AddTokenWindow
from presentation.delete_token_window import DeleteTokenWindow


class MainWindow(QMainWindow):
    def __init__(self, session_maker: SQLiteSessionMaker, crypto_getter: CryptoCurrencyGetter) -> None:
        super().__init__()

        self.session_maker = session_maker
        self.crypto_getter = crypto_getter
        self.refresh_window()

        self.data = crypto_getter.get_currencies()
        self.names = crypto_getter.get_currencies_names(self.data)
        self.prices = get_desired_currencies_price(self.data, self.names)
        self.header_labels = [
            "Токен", "Количество", "Цена покупки", "Изменение цены", "Текущая цена", "Дата добавления", "Биржа"
        ]

        uic.loadUi("resources/main_window.ui", self)
        self.pushButton.clicked.connect(self.add_token)
        self.pushButton_3.clicked.connect(self.delete_token)

    def refresh_window(self) -> None:
        connection = self.session_maker.create_connection()
        cur = connection.cursor()
        previous_table = CryptoCurrencyRepository(cur).read_currencies_table()
        connection.close()

        previous_table = [list(elem)[1:] for elem in previous_table]
        self.table = actualize_table(previous_table, self.crypto_getter)

    def fill_table(self) -> None:
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(len(self.table))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(self.header_labels)

        for r, row in enumerate(self.table):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(r, c, item)

    def add_token(self) -> None:
        self.add_token_window = AddTokenWindow(self.prices, self.session_maker)
        self.add_token_window.exec()
        self.refresh_window()
        self.fill_table()

    def delete_token(self) -> None:
        row = self.tableWidget.currentRow()
        if row >= 0:
            token = self.table[row]
            self.delete_token_window = DeleteTokenWindow(token, self.session_maker)
            self.delete_token_window.exec()
            self.refresh_window()
            self.fill_table()

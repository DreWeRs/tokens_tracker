from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QMessageBox, QErrorMessage

from application.get_date import get_date
from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository


class AddTokenWindow(QDialog):
    def __init__(self, prices: dict[str, float], session_maker: SQLiteSessionMaker) -> None:
        super().__init__()
        uic.loadUi("resources/add_token_window.ui", self)
        self.prices = prices
        self.session_maker = session_maker

        self.price_state = False
        self.date_state = True
        for key in self.prices.keys():
            self.chooseBox.addItem(key, userData=str(self.prices[key]))
        self.dateEdit.setDate(QDate(*get_date()))
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавления токена')
        self.setWindowIcon(QIcon('resources/icons/bill_icon.png'))
        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.close)

        self.realPriceBox.stateChanged.connect(self.price_mark_changed)
        self.dateMarkBox.stateChanged.connect(self.date_mark_changed)

    def execute(self) -> None:
        connection = self.session_maker.create_connection()
        cursor = connection.cursor()

        crypto_currency = {'name': self.chooseBox.currentText(),
                           'buy_price': float(self.priceSpinBox.value()),
                           'date': str(self.dateEdit.text()),
                           'amount': float(self.amountBox.value()),
                           'market': self.marketLine.text()
                           }

        CryptoCurrencyRepository(cursor=cursor).write_new_currency(crypto_currency)
        connection.commit()
        connection.close()
        self.close()

    def price_mark_changed(self) -> None:
        self.price_state = self.realPriceBox.isChecked()
        if self.price_state:
            self.priceSpinBox.setDisabled(True)
            self.priceSpinBox.setValue(float(self.chooseBox.currentData()))
        else:
            self.priceSpinBox.setEnabled(True)
            self.priceSpinBox.setValue(0)

    def date_mark_changed(self) -> None:
        self.date_state = self.dateMarkBox.isChecked()
        if self.date_state:
            self.dateEdit.setDisabled(True)
            self.dateEdit.setDate(QDate(*get_date()))
        else:
            self.dateEdit.setEnabled(True)

from PyQt6 import uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

from application.get_date import get_date
from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository


class EditTokenWindow(QDialog):
    def __init__(self, token: list[str | float], session_maker: SQLiteSessionMaker) -> None:
        super().__init__()
        uic.loadUi("resources/edit_token_window.ui", self)
        self.token = token
        self.session_maker = session_maker

        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.close)

        self.date_state = True
        self.dateMarkBox.stateChanged.connect(self.date_mark_changed)
        self.dateEdit.setDate(QDate(*get_date()))

        self.priceSpinBox.setValue(token[2])
        self.amountBox.setValue(token[1])
        self.marketLine.setText(token[-1])

    def execute(self):
        connection = self.session_maker.create_connection()
        cursor = connection.cursor()

        crypto_currency = {'name': self.token[0]}
        try:
            crypto_currency['buy_price'] = float(self.priceSpinBox.value())
        except TypeError:
            msg = QMessageBox()  # Срочно переделать сделав месадж бокс объектом
            msg.setText('Неверная цена')
            msg.setInformativeText('Цена должна быть числом')
            msg.exec()
        crypto_currency['date'] = str(self.dateEdit.text())
        try:
            crypto_currency['amount'] = float(self.amountBox.value())
        except TypeError:
            msg = QMessageBox()  # Срочно переделать сделав месадж бокс объектом
            msg.setText('Неверное количество')
            msg.setInformativeText('Количество должно быть числом')
            msg.exec()
        crypto_currency['market'] = self.marketLine.text()

        CryptoCurrencyRepository(cursor=cursor).edit_currency(crypto_currency)
        connection.commit()
        connection.close()
        self.close()

    def date_mark_changed(self) -> None:
        self.date_state = self.dateMarkBox.isChecked()
        if self.date_state:
            self.dateEdit.setDisabled(True)
            self.dateEdit.setDate(QDate(*get_date()))
        else:
            self.dateEdit.setEnabled(True)

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap

from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository


class DeleteTokenWindow(QDialog):
    def __init__(self, token: list[str], session_maker: SQLiteSessionMaker) -> None:
        super().__init__()
        uic.loadUi("resources/delete_token_window.ui", self)
        self.token = token
        self.session_maker = session_maker

        pixmap = QPixmap("resources/icons/delete_picture.png").scaled(151, 151)
        self.imageLabel.setPixmap(pixmap)
        self.msgLabel.setText(f'Вы хотите удалить: {token[0]}?')

        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.close)

    def execute(self) -> None:
        connection = self.session_maker.create_connection()
        cursor = connection.cursor()

        CryptoCurrencyRepository(cursor).delete_currency(self.token[0])

        connection.commit()
        connection.close()
        self.close()

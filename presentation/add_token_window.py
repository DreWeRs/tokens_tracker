from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from infrastructure.db.db_setup import SQLiteSessionMaker


class AddTokenWindow(QDialog):
    def __init__(self, session_maker: SQLiteSessionMaker) -> None:
        super().__init__()
        uic.loadUi("resources/add_token_window.ui", self)
        self.session_maker = session_maker

        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.close)

    def execute(self):
        ...  # Нужно доделать

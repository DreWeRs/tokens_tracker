from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class AddTokenWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("resources/add_token_window.ui", self)
        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.close)

    def execute(self):
        ...  # Need to realize

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget


class AddTokenWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/add_token_window.ui', self)
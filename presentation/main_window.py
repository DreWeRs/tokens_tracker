from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from presentation.add_token_window import AddTokenWindow


class MainWindow(QMainWindow):
    def __init__(self, table: list[list]) -> None:
        super().__init__()

        self.table = table
        self.header_labels = [
            "Токен", "Цена покупки", "Изменение цены", "Текущая цена", "Дата добавления",
        ]

        uic.loadUi("resources/main_window.ui", self)
        self.pushButton.clicked.connect(self.add_token)
        self.pushButton_2.clicked.connect(self.fill_table)  # temporary solve

    def fill_table(self) -> None:
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setRowCount(len(self.table))
        self.tableWidget.setColumnCount(len(self.table[0]))
        self.tableWidget.setHorizontalHeaderLabels(self.header_labels)

        for r, row in enumerate(self.table):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(r, c, item)

    def add_token(self) -> None:
        self.add_token_window = AddTokenWindow()
        self.add_token_window.show()

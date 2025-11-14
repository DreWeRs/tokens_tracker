import csv

from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog

from application.actualize_table import actualize_table
from application.get_crypto_currency import CryptoCurrencyGetter, get_desired_currencies_price
from application.get_date import get_date
from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.balance_logs_repository import BalanceLogsRepository
from infrastructure.db.repositories.crypto_currency_repository import CryptoCurrencyRepository
from presentation.add_token_window import AddTokenWindow
from presentation.delete_token_window import DeleteTokenWindow
from presentation.edit_token_window import EditTokenWindow
from presentation.graph_window import GraphWindow


class MainWindow(QMainWindow):
    def __init__(self, session_maker: SQLiteSessionMaker, crypto_getter: CryptoCurrencyGetter) -> None:
        super().__init__()
        uic.loadUi("resources/main_window.ui", self)
        self.session_maker = session_maker
        self.crypto_getter = crypto_getter
        self.refresh_window()

        self.data = crypto_getter.get_currencies()
        self.names = crypto_getter.get_currencies_names(self.data)
        self.prices = get_desired_currencies_price(self.data, self.names)
        self.header_labels = [
            "Токен", "Количество", "Цена покупки", "Изменение цены", "Текущая цена", "Дата добавления", "Биржа"
        ]
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.add_token)
        self.pushButton_2.clicked.connect(self.edit_token)
        self.pushButton_3.clicked.connect(self.delete_token)

        menu = self.menuBar()

        file_menu = menu.addMenu('Файл')
        save_action = QAction('Выгрузить в CSV-файл', self)
        save_action.triggered.connect(self.upload_to_csv)
        file_menu.addAction(save_action)

        data_menu = menu.addMenu('Данные')
        graph_action = QAction('График изменения баланса', self)
        graph_action.triggered.connect(self.display_graph)
        data_menu.addAction(graph_action)

    def refresh_window(self) -> None:
        connection = self.session_maker.create_connection()
        cur = connection.cursor()
        previous_table = CryptoCurrencyRepository(cur).read_currencies_table()
        connection.close()

        previous_table = [list(elem)[1:] for elem in previous_table]
        self.table = actualize_table(previous_table, self.crypto_getter)

        all_tokens_sum = sum([x[4] * x[1] for x in self.table])
        buy_sum = sum([x[2] for x in self.table])
        self.sumLabel.setText(f'Общая сумма: {all_tokens_sum:.4f}$')
        self.difLabel.setText(f'Изменение баланса: {((all_tokens_sum - buy_sum) / buy_sum * 100):.4f}%')

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

    def edit_token(self) -> None:
        row = self.tableWidget.currentRow()
        if row >= 0:
            token = self.table[row]
            self.edit_token_window = EditTokenWindow(token, self.session_maker)
            self.edit_token_window.exec()
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

    def upload_to_csv(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить как CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.header_labels)
            for r in range(len(self.table)):
                row = []
                for c in range(len(self.table[r])):
                    item = self.table[r][c]
                    row.append(item)

                writer.writerow(row)

    def display_graph(self) -> None:
        self.graph_window = GraphWindow(self.session_maker)
        self.graph_window.show()

    def logging(self) -> None:
        connection = self.session_maker.create_connection()
        cursor = connection.cursor()

        balance = self.sumLabel.text().split()[-1][:-1]
        raw_date = get_date()
        date = '.'.join([str(x) for x in raw_date])

        logs_repository = BalanceLogsRepository(cursor=cursor)
        if logs_repository.check_unique_log(date):
            logs_repository.write_new_balance(float(balance), date)

        connection.commit()
        connection.close()

from datetime import datetime

import pyqtgraph
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from infrastructure.db.db_setup import SQLiteSessionMaker
from infrastructure.db.repositories.balance_logs_repository import BalanceLogsRepository


class GraphWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self, session_maker: SQLiteSessionMaker) -> None:
        super().__init__()
        self.session_maker = session_maker

        self.setWindowTitle('График баланса')
        self.setWindowIcon(QIcon('resources/icons/icon_chartup.png'))

        layout = QVBoxLayout(self)
        self.graphWidget = pyqtgraph.PlotWidget(axisItems={'bottom': pyqtgraph.DateAxisItem()})
        layout.addWidget(self.graphWidget)

        self.setup_plot()
        self.build_graph()

    def setup_plot(self) -> None:
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Баланс', units='$')
        self.graphWidget.setLabel('bottom', 'Дата')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle("Изменение баланса по датам", color='k', size='14pt')

    def build_graph(self) -> None:
        connection = self.session_maker.create_connection()
        cursor = connection.cursor()

        logs = BalanceLogsRepository(cursor=cursor).read_logs()
        dates = [log[2] for log in logs]
        balances = [float(log[1]) for log in logs]

        timestamps = []
        for date in dates:
            dt_object = datetime.strptime(date, "%Y.%m.%d")
            timestamps.append(dt_object.timestamp())

        self.graphWidget.plot(timestamps, balances,
                              pen=pyqtgraph.mkPen(color='blue', width=2),
                              symbol='o', symbolSize=4, symbolBrush='blue', style=QtCore.Qt.PenStyle.SolidLine)

        for i, (timestamp, balance, date) in enumerate(zip(timestamps, balances, dates)):
            text = pyqtgraph.TextItem(f"{balance} $\n{date}", color='k', anchor=(0.5, 1.5))
            self.graphWidget.addItem(text)
            text.setPos(timestamp, balance)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

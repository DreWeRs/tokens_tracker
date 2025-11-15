import sqlite3
from dataclasses import dataclass


@dataclass
class BalanceLogsRepository:
    cursor: sqlite3.Cursor

    def read_logs(self) -> list[tuple]:
        query = """SELECT * FROM balances"""

        logs = self.cursor.execute(query).fetchall()

        return logs

    def write_new_balance(self, balance: float, date: str) -> None:
        query = """
        INSERT INTO balances (balance, date)
        VALUES (?, ?)
        """
        params = (balance, date)

        self.cursor.execute(query, params)

    def check_unique_log(self, date: str):
        query = """
        SELECT * FROM balances
        WHERE date = ?
        """
        params = (date,)

        result = self.cursor.execute(query, params).fetchone()
        if result:
            return False
        return True

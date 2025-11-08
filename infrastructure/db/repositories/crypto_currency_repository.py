import sqlite3
from dataclasses import dataclass


@dataclass
class CryptoCurrencyRepository:
    cursor: sqlite3.Cursor

    def read_currencies_table(self) -> list[list]:
        query = '''SELECT * FROM tokens'''

        table = self.cursor.execute(query).fetchall()

        return table

    def write_new_currency(self, crypto_currency: dict) -> None:  # Вот тут надо переделать, скорее всего вместо
        # аргумента-словаря будет аргумент-объект
        query = '''
        INSERT INTO tokens (name, amount, buy_price, date, market) 
        VALUES (?, ?, ?, ?, ?)
        '''
        params = (crypto_currency['name'],
                  crypto_currency['amount'],
                  crypto_currency['buy_price'],
                  crypto_currency['date'],
                  crypto_currency['market']
                  )

        self.cursor.execute(query, params)

    def edit_currency(self, crypto_currency: dict) -> None:
        query = '''UPDATE tokens SET amount=?, buy_price=?, date=?, market=?
        WHERE name = ?
        '''
        params = (crypto_currency['amount'],
                  crypto_currency['buy_price'],
                  crypto_currency['date'],
                  crypto_currency['market'],
                  crypto_currency['name']
                  )

        self.cursor.execute(query, params)

    def delete_currency(self, currency_name: str) -> None:
        query = '''DELETE FROM tokens
        WHERE name=?'''
        params = (currency_name,)

        self.cursor.execute(query, params)

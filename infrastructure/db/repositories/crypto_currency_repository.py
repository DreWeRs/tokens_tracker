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
        INSERT INTO tokens (name, amount, buy_price, difference, current_price, date, market) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (crypto_currency['name'],
                  crypto_currency['amount'],
                  crypto_currency['buy_price'],
                  crypto_currency['difference'],
                  crypto_currency['current_price'],
                  crypto_currency['date'],
                  crypto_currency['market']
                  )

        self.cursor.execute(query, params)

    def change_price_fields(self, table: list[list]) -> None:
        query = '''UPDATE tokens SET buy_price=?, difference=?, current_price=?'''
        for _ in range(len(table)):
            params = (table[3], table[4])
            self.cursor.execute(query, params)

    def edit_currency(self, crypto_currency: dict) -> None:
        query = '''UPDATE tokens SET amount=?, buy_price=?, difference=?, current_price=?, date=?, market=?'''
        params = (crypto_currency['amount'],
                  crypto_currency['buy_price'],
                  crypto_currency['difference'],
                  crypto_currency['current_price'],
                  crypto_currency['date'],
                  crypto_currency['market']
                  )

        self.cursor.execute(query, params)

    def delete_currency(self, currency_name: str) -> None:
        query = '''DELETE FROM tokens
        WHERE name=?'''
        params = (currency_name,)

        self.cursor.execute(query, params)

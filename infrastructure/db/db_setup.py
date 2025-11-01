import sqlite3
from dataclasses import dataclass

from config import Config


@dataclass
class SQLiteSessionMaker:
    config: Config

    def create_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.config.db_name)

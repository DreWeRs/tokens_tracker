import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    url: str
    db_name: str


def load_config() -> Config:
    load_dotenv()

    url = os.environ["URL"]
    db_name = os.environ["DB_NAME"]
    return Config(url, db_name)

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    url: str


def load_config() -> Config:
    load_dotenv()

    url = os.environ["URL"]
    return Config(url)

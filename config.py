import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    api_key: str
    url: str

    def get_url(self) -> str:
        return self.url + self.api_key


def load_config() -> Config:
    load_dotenv()

    api_key = os.getenv('API_KEY')
    url = os.getenv('URL')
    return Config(api_key, url)

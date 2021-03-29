from typing import List

import yaml
from pathlib import Path

class Config:
    def __init__(self):
        with open(Path(__file__).resolve().parent.parent / "config.yml", "r") as stream:
            self.data = yaml.safe_load(stream)

    @property
    def webhook_url(self) -> str:
        return self.data['webhook_url']

    @property
    def users(self) -> List[str]:
        return self.data['users']

    @property
    def delay(self) -> int:
        return self.data['delay']


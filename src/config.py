import yaml
from typing import List
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

    @property
    def content(self) -> str:
        return self.data['content']

    @property
    def login_username(self) -> str:
        return self.data['login_username']

    @property
    def login_password(self) -> str:
        return self.data['login_password']

    @property
    def skip_first_run(self) -> bool:
        return 'skip_first_run' in self.data and self.data['skip_first_run'] == 'true'

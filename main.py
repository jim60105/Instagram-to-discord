import sys
import time
from typing import List

from src.db import DB
from src.config import Config
from src.loop import Loop
from src.loader import Loader


if __name__ == "__main__":
    print('== Instagram to Discord ==')
    config = Config()

    if len(config.users) == 0 or not config.webhook_url:
        print('Please set the config file properly!', file=sys.stderr)
        exit()

    DB.init_db()

    L = Loader(config.login_username, config.login_password)

    loops: List[Loop] = []
    for username in config.users:
        print(f'Add monitor: {username}')
        loops.append(Loop(config, username, L))

    delay = config.delay or 300
    print(f'Interval: {delay} seconds.')
    print(f'Complete initialization. Start monitoring...')
    while True:
        for loop in loops:
            time.sleep(delay)
            loop.run()

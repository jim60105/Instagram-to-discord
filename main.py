import time

from src.db import DB
from src.config import Config
from src.loop import Loop
from src.loader import Loader


if __name__ == "__main__":
    config = Config()

    if len(config.users) == 0 or not config.webhook_url:
        print('Please set the config file properly!')
        exit()

    DB.init_db()

    L = Loader(config.login_username, config.login_password)

    print('Project start!')

    loops = []
    for username in config.users:
        print(f'Add monitor: {username}')
        loops.append(Loop(config, username, L))

    while True:
        for loop in loops:
            loop.run()
        time.sleep(config.delay or 600)

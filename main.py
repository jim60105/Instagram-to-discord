import time

from src.config import Config
from src.loop import Loop
from src.loader import loader


if __name__ == "__main__":
    config = Config()

    if len(config.users) == 0 or not config.webhook_url:
        print('Please set the config file properly!')
        exit()
        
    L = loader(config.login_username, config.login_password)

    loops = []
    for username in config.users:
        loops.append(Loop(config, username, L))

    while True:
        for loop in loops:
            loop.run()
        time.sleep(config.delay or 600)

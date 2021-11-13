import time
from src.config import Config
from src.loop import Loop


if __name__ == "__main__":
    config = Config()

    if len(config.users) == 0 or not config.webhook_url:
        print('Please set the config file properly!')
        exit()

    users = []
    for u in config.users:
        users.append(Loop(config, u))

    while True:
        for user in users:
            user.run()
        time.sleep(config.delay or 600)

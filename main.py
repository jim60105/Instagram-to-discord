import time
import os

from dhooks.client import Webhook

from src.config import Config
from src.loop import Loop

if __name__ == "__main__":
    config = Config()

    if len(config.users) == 0 or not config.webhook_url:
        print('Please set the config file properly!')
        exit()

    users = []
    for u in config.users:
        last_image = os.getenv('LAST_IMAGE_ID_' + u)
        last_story = os.getenv('LAST_STORY_ID_' + u)

        users.append(Loop(config, u, last_image, last_story))

    while True:
        for user in users:
            user.run()
        time.sleep(config.delay or 600)

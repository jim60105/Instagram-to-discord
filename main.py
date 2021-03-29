import time

from src.config import Config
from src.loop import Loop

from pathlib import Path

if __name__ == "__main__":
    config = Config()

    # Load last_image
    last_image = None
    last_image_path = Path(__file__).resolve().parent / 'last_image'
    if last_image_path.exists():
        with open(last_image_path, 'r') as f:
            last_image = f.read().strip()

    users = [Loop(config, u, last_image) for u in config.users]

    while True:
        for user in users:
            user.run()
        time.sleep(config.delay)

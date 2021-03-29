from dhooks import Webhook
import dhooks

from src.config import Config
from src.instagram.post import Post
from src.instagram.scraper import Scraper
from src.instagram.user import User

from pathlib import Path

class Loop:
    def __init__(self, config: Config, username, last_image):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.last_image = last_image

    def run(self):
        scraper = Scraper(self.username)
        if scraper.status != 200:
            print(f"Got invalid response code: {scraper.status}")
            return

        post = scraper.get_last_post()
        user = scraper.get_user()

        if post.id == self.last_image:
            return

        with open(Path(__file__).resolve().parent.parent / ('last_image_'+self.username), 'w') as f:
            f.write(post.id)

        embed = self.__create_embed(post, user)
        print(f'New post found\n{user.name} : {post.id}')
        self.webhook.send(embed=embed)
        self.last_image = post.id

    @staticmethod
    def __create_embed(post: Post, user: User) -> dhooks.Embed:
        embed = dhooks.Embed(description=post.caption)
        embed.color = 0xEC054C
        embed.set_image(post.image_url)
        embed.set_timestamp(time=post.timestamp)
        embed.set_footer(f'❤️ {post.likes} | 💬 {post.comments}')
        embed.set_author(name=user.name, icon_url=user.icon_url, url=user.link)

        return embed

from dhooks import Webhook, Embed
from instaloader import Post, Profile
from pathlib import Path

from src.config import Config
from src.scraper import Scraper


class Loop:
    def __init__(self, config: Config, username, last_image):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.last_image = last_image
        self.login_username = config.login_username
        self.login_password = config.login_password

    def run(self):
        scraper = Scraper(self.username,
                          self.login_username, self.login_password)

        post = scraper.get_last_post()
        profile = scraper.get_profile()

        if post is None or str(post.mediaid) == str(self.last_image):
            return

        with open(Path(__file__).resolve().parent.parent / ('last_image_'+self.username), 'w') as f:
            f.write(str(post.mediaid))

        embed = self.__create_embed(post, profile)
        print(f'New post found\n{profile.username} : {post.mediaid}')
        self.webhook.send(embed=embed)
        self.last_image = post.mediaid

    @staticmethod
    def __create_embed(post: Post, profile: Profile) -> Embed:
        embed = Embed(description=post.caption)
        embed.color = 0xEC054C
        embed.set_image(post.url)
        embed.set_timestamp(time=post.date_utc)
        embed.set_footer(f'❤️ {post.likes} | 💬 {post.comments}')
        embed.set_author(name=profile.username, icon_url=profile.profile_pic_url,
                         url=f'https://www.instagram.com/{profile.userid}')

        return embed

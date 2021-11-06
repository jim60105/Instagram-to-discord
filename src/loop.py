from types import NoneType
from dhooks import Webhook, Embed
from instaloader import Post
from instaloader.structures import StoryItem
from pathlib import Path

from src.config import Config
from src.scraper import Scraper


class Loop:
    def __init__(self, config: Config, username: str,
                 last_image: str | NoneType, last_story: str | NoneType):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.last_image = last_image
        self.last_story = last_story
        self.login_username = config.login_username
        self.login_password = config.login_password

    def run(self):
        scraper = Scraper(self.username,
                          self.login_username, self.login_password)

        # Post
        post = scraper.get_last_post()
        if post is not None and str(post.mediaid) != str(self.last_image):
            with open(Path(__file__).resolve().parent.parent / ('last_image_'+self.username), 'w') as f:
                f.write(str(post.mediaid))

            profile = post.owner_profile
            embed = self.__create_embed(post)
            print(f'New post found\n{profile.username} : {post.mediaid}')
            self.webhook.send(f'https://www.instagram.com/p/{post.shortcode}',
                              embed,
                              avatar_url=profile.profile_pic_url)
            self.last_image = post.mediaid

        # Story
        storyItem = scraper.get_last_storyItem()
        if storyItem is not None and str(storyItem.mediaid) != str(self.last_story):
            with open(Path(__file__).resolve().parent.parent / ('last_story_'+self.username), 'w') as f:
                f.write(str(storyItem.mediaid))

            profile = storyItem.owner_profile
            embed = self.__create_embed(storyItem)
            print(f'New story found\n{profile.username} : {storyItem.mediaid}')
            self.webhook.send(f'https://www.instagram.com/stories/{profile.username}/{storyItem.mediaid}/',
                              embed,
                              avatar_url=profile.profile_pic_url)
            self.last_story = storyItem.mediaid

    @staticmethod
    def __create_embed(item: Post | StoryItem) -> Embed:
        profile = item.owner_profile
        embed = Embed()

        if item is Post:
            embed.description = item.caption
            embed.set_footer(f'❤️ {item.likes} | 💬 {item.comments}')

        embed.color = 0xEC054C
        embed.set_image(item.url)
        embed.set_timestamp(time=item.date_utc)
        embed.set_author(name=profile.username, icon_url=profile.profile_pic_url,
                         url=f'https://www.instagram.com/{profile.username}')

        return embed

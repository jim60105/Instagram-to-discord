import os
import requests
from typing import Any
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
from dhooks import Webhook, File
from instaloader import Post
from instaloader.structures import StoryItem

from src.config import Config
from src.scraper import Scraper


class Loop:
    def __init__(self, config: Config, username: str,
                 last_image: str | NoneType, last_story: str | NoneType):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.last_image = last_image
        self.last_story = last_story
        self.content = config.content
        self.login_username = config.login_username
        self.login_password = config.login_password
        self.scraper = Scraper(self.username,
                          self.login_username, self.login_password)

        self.first_run = config.skip_first_run

    def run(self):
        if self.first_run:
            self.__do_first_run()
            return

        # Post
        post = self.scraper.get_last_post()
        if post is not None and str(post.mediaid) != str(self.last_image):
            profile = post.owner_profile
            embed = self.__create_embed(post)
            print(f'New post found\n{profile.username} : {post.mediaid}')
            self.webhook.send(f'{self.content}\nhttps://www.instagram.com/p/{post.shortcode}',
                              embed,
                              avatar_url=profile.profile_pic_url)
            self.last_image = post.mediaid
            envName = 'LAST_IMAGE_ID_' + self.username
            os.environ[envName] = str(self.last_image)

        if self.scraper.is_login:
            # Story
            storyItem = self.scraper.get_last_storyItem()
            if storyItem is not None and str(storyItem.mediaid) != str(self.last_story):
                profile = storyItem.owner_profile
                embed = self.__create_embed(storyItem)
                print(
                    f'New story found\n{profile.username} : {storyItem.mediaid}')
                self.webhook.send(f'{self.content}\nhttps://www.instagram.com/stories/{profile.username}/{storyItem.mediaid}/',
                                  embed,
                                  avatar_url=profile.profile_pic_url)
                self.last_story = storyItem.mediaid
                envName = 'LAST_STORY_ID_' + self.username
                os.environ[envName] = str(self.last_story)

    @staticmethod
    def __create_embed(item: Post | StoryItem) -> Embed:
        profile = item.owner_profile
        embed = Embed()

        if type(item) is Post:
            embed.description = item.caption
            embed.set_footer(f'❤️ {item.likes} | 💬 {item.comments}')

        embed.color = 0xEC054C
        embed.set_image(item.url)
        embed.set_timestamp(time=item.date_utc)
        embed.set_author(name=profile.username,# icon_url=profile.profile_pic_url,
                         url=f'https://www.instagram.com/{profile.username}')
        embed.set_thumbnail(profile.profile_pic_url)
    def __do_first_run(self) -> bool:
        if os.environ['FIRST_RUN'] == 'false':
            self.first_run = 0
            return

        post = self.scraper.get_last_post()
        if post is Post:
            os.environ['LAST_IMAGE_ID_' + self.username] = str(post.mediaid)
        storyItem = self.scraper.get_last_storyItem()
        if storyItem is StoryItem:
            os.environ['LAST_STORY_ID_' +
                       self.username] = str(storyItem.mediaid)
        print(f'SKIP FIRST RUN!')
        self.first_run = 0
        os.environ['FIRST_RUN'] = 'false'

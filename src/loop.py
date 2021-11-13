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
    def __init__(self, config: Config, username: str):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
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
        envName = 'LAST_IMAGE_ID_' + self.username
        last_image = os.getenv(envName)
        post = self.scraper.get_last_post()
        if post is not None and str(post.mediaid) != str(last_image):
            profile = post.owner_profile
            print(f'New post found\n{profile.username} : {post.mediaid}')
            with NamedTemporaryFile() as temp:
                file = self.__create_File(post, temp)
                self.webhook.send(f'{self.content}\n{post.caption}\nhttps://www.instagram.com/p/{post.shortcode}'
                                  if self.content != ''
                                  else f'{post.caption}\nhttps://www.instagram.com/p/{post.shortcode}',
                                  file=file,
                                  username=f'[Instagram] {profile.full_name} ({profile.username})'
                                  if profile.full_name != profile.username
                                  else f'[Instagram] {profile.full_name}',
                                  avatar_url=profile.profile_pic_url)
            os.environ[envName] = str(post.mediaid)

        if self.scraper.should_login:
            # Story
            envName = 'LAST_STORY_ID_' + self.username
            last_story = os.getenv(envName)
            storyItem = self.scraper.get_last_storyItem()
            if storyItem is not None and str(storyItem.mediaid) != str(last_story):
                profile = storyItem.owner_profile
                print(
                    f'New story found\n{profile.username} : {storyItem.mediaid}')
                with NamedTemporaryFile() as temp:
                    file = self.__create_File(storyItem, temp)
                    self.webhook.send(f'{self.content}\nhttps://www.instagram.com/stories/{profile.username}/{storyItem.mediaid}/'
                                      if self.content != ''
                                      else f'https://www.instagram.com/stories/{profile.username}/{storyItem.mediaid}/',
                                      file=file,
                                      username=f'[Instagram] {profile.full_name} ({profile.username})'
                                      if profile.full_name != profile.username
                                      else f'[Instagram] {profile.full_name}',
                                      avatar_url=profile.profile_pic_url)
                os.environ[envName] = str(storyItem.mediaid)

    @staticmethod
    def __create_File(item: Post | StoryItem, file: Any) -> File:
        url = item.video_url if item.is_video else item.url

        file.write(requests.get(url).content)
        path = urlparse(url).path
        file.flush()
        file.seek(0)
        filename = os.path.basename(path)
        return File(file, filename)

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

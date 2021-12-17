import os
import requests
from typing import Any
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile
from dhooks import Webhook, File
from instaloader import Post
from instaloader.structures import StoryItem

from src.db import DB
from src.config import Config
from src.scraper import Scraper
from src.loader import Loader


class Loop:
    def __init__(self, config: Config, username: str, loader: Loader):
        self.webhook = Webhook(config.webhook_url)
        self.username = username
        self.content = config.content
        self.loader = loader
        self.scraper = Scraper(username, loader)
        self.__log_to_db_onInit()

    def run(self):
        with DB(readonly=True) as db:
            # Post
            posts = self.scraper.get_posts()
            post = next(posts, None)
            while post is not None and not db.get_exist(post.owner_id, post.mediaid):
                profile = post.owner_profile
                print(
                    f'New post found\n{profile.username}({post.owner_id}) : {post.mediaid}')
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
                DB(readonly=False).insert(post.owner_id, post.mediaid)
                post = next(posts, None)

            # Story
            if self.loader.should_login:
                story = self.scraper.get_last_story()
                if story is None:
                    return

                storyItems = story.get_items()
                storyItem = next(storyItems, None)
                while storyItem is not None and not db.get_exist(storyItem.owner_id, storyItem.mediaid):
                    profile = storyItem.owner_profile
                    print(
                        f'New story found\n{profile.username}({storyItem.owner_id}) : {storyItem.mediaid}')
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
                    DB(readonly=False).insert(
                        storyItem.owner_id, storyItem.mediaid)
                    storyItem = next(storyItems, None)

    @staticmethod
    def __create_File(item: Post | StoryItem, file: Any) -> File:
        url = item.video_url if item.is_video else item.url

        file.write(requests.get(url).content)
        path = urlparse(url).path
        file.flush()
        file.seek(0)
        filename = os.path.basename(path)
        return File(file, filename)

    def __log_to_db_onInit(self):
        with DB(readonly=False) as db:
            if not db.is_empty(self.scraper.profile.userid):
                print(f'Database is not empty on user {self.scraper.profile.username}')
                print(f'Skip log old content to database.')
                return

            post = self.scraper.get_last_post()
            if post is not None:
                db.insert(post.owner_id, post.mediaid)
                print(
                    f'Old post found\n{post.owner_username}({post.owner_id}) : {post.mediaid}')
            storyItem = self.scraper.get_last_storyItem()
            if storyItem is not None:
                db.insert(storyItem.owner_id, storyItem.mediaid)
                print(
                    f'Old story found\n{storyItem.owner_username}({storyItem.owner_id}) : {storyItem.mediaid}')

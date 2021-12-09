from types import NoneType
from typing import Iterator
from instaloader.structures import Story, StoryItem
import requests
import time
from instaloader import Post, Profile, NodeIterator

from loader import loader


class Scraper:
    def __init__(self, username: str, loader: loader):
        self.loader = loader

        self.profile = self.__get_profile(username)

    def __get_profile(self, username: str) -> Profile:
        try:
            return Profile.from_username(self.loader.context, username)
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            return self.__get_profile(username)

    def get_last_post(self) -> Post | NoneType:
        return next(self.get_posts(), None)

    def get_posts(self) -> NodeIterator[Post]:
        post = self.profile.get_posts()
        return post

    def get_profile(self) -> Profile:
        return self.profile

    def get_last_storyItem(self) -> StoryItem | NoneType:
        if not self.loader.should_login:
            return None

        if self.loader.test_login() is None:
            self.loader.login()

        story = next(self.get_stories(), None)
        if story is not None:
            return next(story.get_items(), None)
        return None

    def get_stories(self) -> Iterator[Story]:
        return self.loader.get_stories([self.profile.userid])

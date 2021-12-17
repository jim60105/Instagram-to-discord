from instaloader.exceptions import LoginRequiredException
import requests
import time
from types import NoneType
from typing import Iterator
from instaloader import Post, Profile, NodeIterator, instaloader
from instaloader.structures import Story, StoryItem

from src.loader import Loader


class Scraper:
    def __init__(self, username: str, loader: Loader):
        self.loader = loader
        self.username = username
        self.profile = self.__get_profile()

    def __get_profile(self) -> Profile:
        try:
            # Use a new loader to get posts that do not require login.
            self.profile = Profile.from_username(instaloader.Instaloader().context, self.username)
            return self.profile
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            return self.__get_profile()

    def get_last_post(self) -> Post | NoneType:
        return next(self.get_posts(), None)

    def get_posts(self) -> NodeIterator[Post]:
        return self.__get_profile().get_posts()

    def get_profile(self) -> Profile:
        if not self.profile:
            self.__get_profile()
        return self.profile

    def get_last_storyItem(self) -> StoryItem | NoneType:
        story = self.get_last_story()
        if story is not None:
            return next(story.get_items(), None)
        return None

    def get_last_story(self) -> Story | NoneType:
        if not self.loader.should_login:
            return None

        try:
            story = next(self.get_stories(), None)
        except LoginRequiredException:
            self.loader.login()
            story = next(self.get_stories(), None)

        return story

    def get_stories(self) -> Iterator[Story]:
        return self.loader.get_stories([self.profile.userid])

from types import NoneType
from typing import Iterator
from instaloader.structures import Story, StoryItem
import requests
import time
from instaloader import instaloader, Post, Profile, NodeIterator

L: instaloader.Instaloader = instaloader.Instaloader()


class Scraper:
    is_login: bool = 0

    def __init__(self, username: str, login_username: str, login_password: str):
        if login_username and login_password:
            try:
                self.is_login = L.test_login() is not None
            except instaloader.LoginRequiredException:
                self.is_login = 0

            if not self.is_login:
                L.login(login_username, login_password)
                print(f'Login as {login_username}')
                self.is_login = L.test_login() is not None

        self.profile = self.__get_profile(username)

    def __get_profile(self, username: str) -> Profile:
        try:
            return Profile.from_username(L.context, username)
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            return Scraper.__get_profile(username)

    def get_last_post(self) -> Post | NoneType:
        return next(self.get_posts(), None)

    def get_posts(self) -> NodeIterator[Post]:
        post = self.profile.get_posts()
        return post

    def get_profile(self) -> Profile:
        return self.profile

    def get_last_storyItem(self) -> StoryItem | NoneType:
        if not self.is_login:
            return None

        story = next(self.get_stories(), None)
        if story is not None:
            return next(story.get_items(), None)
        return None

    def get_stories(self) -> Iterator[Story]:
        if self.is_login:
            return L.get_stories([self.profile.userid])
        else:
            return None

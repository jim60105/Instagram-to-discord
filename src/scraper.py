from types import NoneType
from typing import Iterator
from instaloader.structures import Story, StoryItem
import requests
import time
from instaloader import instaloader, Post, Profile, NodeIterator


class Scraper:
    def __init__(self, username: str, login_username: str, login_password: str):
        self.L = instaloader.Instaloader()
        if login_username and login_password:
            self.login_username = login_username
            self.login_password = login_password
            self.should_login = self.__login()
        else:
            self.should_login = False

        self.profile = self.__get_profile(username)

    def __get_profile(self, username: str) -> Profile:
        try:
            return Profile.from_username(self.L.context, username)
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            return Scraper.__get_profile(username)

    def __login(self) -> bool:
        logined = False
        try:
            if self.login_username and self.login_password:
                self.L.login(self.login_username, self.login_password)
                logined = self.L.test_login() is not None
        except instaloader.BadResponseException:
            print(f'BadResponceException: This happens when your account is blocked by Instagram. Log in to the app to check what happened.')
        finally:
            if logined:
                print(f'Login as {self.login_username}')
            else:
                print('Login failed')
            return logined

    def get_last_post(self) -> Post | NoneType:
        return next(self.get_posts(), None)

    def get_posts(self) -> NodeIterator[Post]:
        post = self.profile.get_posts()
        return post

    def get_profile(self) -> Profile:
        return self.profile

    def get_last_storyItem(self) -> StoryItem | NoneType:
        if not self.should_login:
            return None
        elif not self.L.test_login():
            if not self.__login():
                return None

        story = next(self.get_stories(), None)
        if story is not None:
            return next(story.get_items(), None)
        return None

    def get_stories(self) -> Iterator[Story]:
        return self.L.get_stories([self.profile.userid])

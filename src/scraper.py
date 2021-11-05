from types import NoneType
import requests
import time
from instaloader import instaloader, Post, Profile, NodeIterator


class Scraper:
    def __init__(self, username: str, login_username: str, login_password: str):
        self.L = instaloader.Instaloader()

        if login_username and login_password:
            self.L.login(login_username, login_password)

        self.profile = self.__get_profile(username)

    def __get_profile(self, username: str) -> Profile:
        try:
            return Profile.from_username(self.L.context, username)
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

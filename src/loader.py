
from instaloader import instaloader


class Loader(instaloader.Instaloader):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        if username and password:
            self.should_login = self.login()

    def login(self) -> bool:
        isLogin = False
        try:
            if self.username and self.password:
                super().login(self.username, self.password)
                isLogin = super().test_login() == self.username
        except instaloader.BadResponseException:
            print(f'BadResponceException: This happens when your account is blocked by Instagram. Log in to the app to check what happened.')
        finally:
            if isLogin:
                print(f'Login as {self.username}')
            else:
                print('Login failed')
            return isLogin

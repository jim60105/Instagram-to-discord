import sys
from instaloader import instaloader


class Loader(instaloader.Instaloader):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.should_login = self.login()

    def login(self) -> bool:
        isLogin = False
        try:
            if self.username and self.password:
                super().login(self.username, self.password)
                isLogin = True
        except instaloader.BadResponseException as e:
            print(e, file=sys.stderr)
            print(f'BadResponseException: This happens when your account is blocked by Instagram. Login from your mobile phone app to check what happened.', file=sys.stderr)
        except instaloader.ConnectionException as e:
            print(e, file=sys.stderr)
            print(f'If you get 429, DO NOT login the account {self.username} from multiple instances at the same time. Neither from this program, nor from your mobile phone or PC.', file=sys.stderr)
        except instaloader.TwoFactorAuthRequiredException as e:
            print(e, file=sys.stderr)
            print(f'This program does not support 2FA login. Please disable this feature on account {self.username}.', file=sys.stderr)
        finally:
            if isLogin:
                print(f'Login as {self.username}')
            else:
                print(f'Not login or login failed', file=sys.stderr)
            return isLogin

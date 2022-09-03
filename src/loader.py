import sys
from instaloader import instaloader


class Loader(instaloader.Instaloader):
    def __init__(self, username, password):
        super().__init__(user_agent='Mozilla/5.0 (Linux; Android 10; Mi 9T Pro Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 Instagram 250.0.0.21.109 Android (29/10; 440dpi; 1080x2210; Xiaomi; Mi 9T Pro; raphael; qcom; zh_TW; 394071295)')
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

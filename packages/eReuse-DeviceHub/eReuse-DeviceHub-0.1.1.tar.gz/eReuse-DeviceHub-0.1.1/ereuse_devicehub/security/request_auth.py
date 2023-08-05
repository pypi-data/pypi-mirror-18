import requests
from requests.auth import AuthBase


class Auth(AuthBase):
    """
    Handles the authorization method.

    If there is no available token for us, it logs-in and stores the token. Appends the token to the header accordingly.
    """

    def __init__(self, domain: str, email: str, password: str, login_path: str = 'login', auth_header_title='Basic'):
        self.domain = domain
        self.email = email
        self.password = password
        self.token = None
        self.login_path = login_path
        self.auth_header_title = auth_header_title

    def __call__(self, r):
        if self.token is None:
            self.token = self.login()
        r.headers['Authorization'] = '{} {}'.format(self.auth_header_title, self.token)
        return r

    def login(self):
        account = {
            'email': self.email,
            'password': self.password
        }
        r = requests.post('{}/{}'.format(self.domain, self.login_path), json=account)
        data = r.json()
        return data['token']

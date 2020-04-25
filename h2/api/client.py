from urllib.parse import urljoin
import requests


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class MytargetClient:

    def __init__(self, user, password):
        self.base_url = 'https://target.my.com'

        self.session = requests.Session()
        self.csrf_token = None

        self.user = user
        self.password = password
        self.login()

    def _request(self, method, location, status_code=200, headers=None, params=None, data=None, json=True):
        url = urljoin(self.base_url, location)

        response = self.session.request(method, url, headers=headers, params=params, data=data)

        if response.status_code != status_code:
            raise ResponseStatusCodeException(f' Got {response.status_code} {response.reason} for URL "{url}"')

        if json:
            json_response = response.json()

            if json_response.get('bStateError'):
                error = json_response['sErrorMsg']
                raise RequestErrorException(f'Request "{url}" dailed with error "{error}"!')
            return json_response
        return response

    def login(self):
        location = 'https://auth-ac.my.com/auth/'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'login': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/campaigns/list',
        }

        response = self._request('POST', location, headers=headers, data=data, json=False)
        resp_token = self._request('GET', location, json=False)
        csrf_token = resp_token.headers['Set-Cookie'].split(';')[0].split('=')[-1]
        self.csrf_token = csrf_token
        return response

    def get_main_page(self):
        request = self._request('GET', "campaigns/list", json=False)
        return request

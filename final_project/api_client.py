import requests
from urllib.parse import urljoin
from db.orm_model import User
import random
import string


URL = "http://192.168.0.254/"


class ApiClient:

    def __init__(self):
        self.session = requests.Session()
        payload = {"username": 'DELETE',
                   "password": 'DELETE',
                   "submit": 'Login'}
        random.seed()
        NAME = self.generate_data()
        user = User(username=NAME,
                    password=NAME,
                    email=NAME + "@test.tuu")
        self.user = user
        self.session.post(URL + "login", json=payload)

    def add_user(self, user):
        payload = {"username": user.username,
                   "password": user.password,
                   "email": user.email}
        r = self.session.post(URL + "api/add_user", json=payload)
        return r

    def del_user(self, user):
        r = self.session.get(URL + "api/del_user/" + user.username)
        return r

    def login(self, user):
        payload = {"username": user.username,
                   "password": user.password,
                   "submit": 'Login'}
        r = self.session.post(URL + "login", data=payload)
        return r

    def access_user(self, user, access):
        if access is True:
            r = self.session.get(URL + "api/accept_user/" + user.username)
        else:
            r = self.session.get(URL + "api/block_user/" + user.password)
        return r

    def get_status(self):
        r = requests.get(urljoin(URL, "/status"))
        return r

    def generate_data(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def get_user(self):
        return self.user

    def reg_user(self, name, email, password, repeat_p):
        payload = {"username": name,
                   "email": email,
                   "password": password,
                   "confirm": repeat_p,
                   "term": "y",
                   "submit": "Register"}
        r = requests.post(URL + "reg", json=payload)
        return r

    def login_user(self, name, password):
        payload = {"username": name,
                   "password": password,
                   "submit": "Login"}
        r = requests.post(URL + "login", json=payload)
        return r

from api.http_client import HTTPClient
from config import Endpoints, URL


class Courier(HTTPClient):
    def __init__(self, session, endpoint, user_data):
        super().__init__(session, endpoint)
        self.user_data = user_data
        self.headers = {'Content-Type': 'application/json'}

    def post_user(self):
        url = f"{URL.BASE_URL}{Endpoints.COURIER}"
        response = self.post(
            url, json=self.user_data, headers=self.headers
        )
        return response

    def post_login_users(self, payload: dict | None = None):
        url = f"{URL.BASE_URL}{Endpoints.COURIER_LOGIN}"
        body = payload if payload is not None else self.user_data
        response = self.post(url, json=body, headers=self.headers)
        return response

    def delete_user(self, user_id):
        url = f"{URL.BASE_URL}{Endpoints.COURIER_DELETE}/{user_id}"
        response = self.delete(url, headers=self.headers)
        return response

    def delete_user_without_id(self):
        url = f"{URL.BASE_URL}{Endpoints.COURIER_DELETE}"
        response = self.delete(url, headers=self.headers)
        return response

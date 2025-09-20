from api.http_client import HTTPClient
from config import Endpoints, URL


class Order(HTTPClient):
    def __init__(self, session, endpoint, user_data=None):
        super().__init__(session, endpoint)
        self.user_data = user_data or {}
        self.headers = {'Content-Type': 'application/json'}

    def get_orders(self, order_id):
        response = self.get(
            f'{self.endpoint}{Endpoints.ORDERS}/{order_id}', headers=self.headers
        )
        return response

    def get_orders_list(self, params: dict | None = None):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS}"
        response = self.get(url, headers=self.headers, params=params)
        return response

    def post_order(self, payload: dict | None = None):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS}"
        body = payload if payload is not None else self.user_data
        response = self.post(
            url, json=body, headers=self.headers
        )
        return response

    def track_order(self, track: int):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS_TRACK}"
        response = self.get(url, headers=self.headers, params={"t": track})
        return response

    def track_order_without_number(self):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS_TRACK}"
        response = self.get(url, headers=self.headers)
        return response

    def accept_order(self, order_id: int, courier_id: int):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS_ACCEPT}{order_id}"
        response = self.put(url, headers=self.headers, params={"courierId": courier_id})
        return response

    def accept_order_without_courier(self, order_id: int):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS_ACCEPT}{order_id}"
        response = self.put(url, headers=self.headers)
        return response

    def accept_order_without_order_id(self, courier_id: int):
        url = f"{URL.BASE_URL}{Endpoints.ORDERS_ACCEPT}"  # missing order id in path
        response = self.put(url, headers=self.headers, params={"courierId": courier_id})
        return response

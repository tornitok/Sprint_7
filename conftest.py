from pytest import fixture
from requests import Session

from api.endpoint.courier import Courier
from api.endpoint.order import Order
from config import URL
from utils.order_generator import generate_order_payload
from utils.user_generator import register_new_courier_and_return_login_password


@fixture(scope='session')
def create_session():
    return Session()


@fixture(scope='function')
def create_user():
    user_data = register_new_courier_and_return_login_password()
    return user_data


@fixture(scope='function')
def courier(create_session, create_user):
    return Courier(
        session=create_session, endpoint=URL.BASE_URL, user_data=create_user
    )


@fixture(scope='function')
def order_client(create_session):
    def _make(colors=None):
        payload = generate_order_payload(colors)
        return Order(session=create_session, endpoint=URL.BASE_URL, user_data=payload)

    return _make


@fixture(scope='function')
def order_api(create_session):
    return Order(session=create_session, endpoint=URL.BASE_URL, user_data={})

from http import HTTPStatus
import allure

from api.endpoint.order import Order
from config import URL
from utils.order_generator import generate_order_payload


@allure.feature("Orders")
@allure.story("Track order by number")
@allure.title("Tracking existing order returns order object")
def test_track_order_success_returns_order_object(create_session):
    order = Order(session=create_session, endpoint=URL.BASE_URL)

    with allure.step("Create a new order and get track number"):
        create_resp = order.post_order(generate_order_payload())
        assert create_resp.status_code == HTTPStatus.CREATED
        track = create_resp.json()["track"]

    with allure.step("Track the order by its track number"):
        resp = order.track_order(track)
        assert resp.status_code == HTTPStatus.OK
        body = resp.json()
        assert "order" in body and isinstance(body["order"], dict)


@allure.feature("Orders")
@allure.story("Track order by number")
@allure.title("Tracking without number returns client error")
def test_track_order_without_number_returns_error(create_session):
    order = Order(session=create_session, endpoint=URL.BASE_URL)
    with allure.step("Call track endpoint without 't' parameter"):
        resp = order.track_order_without_number()
        assert 400 <= resp.status_code < 500


@allure.feature("Orders")
@allure.story("Track order by number")
@allure.title("Tracking non-existent number returns client error")
def test_track_order_with_nonexistent_number_returns_error(create_session):
    order = Order(session=create_session, endpoint=URL.BASE_URL)
    with allure.step("Track a clearly non-existent order number"):
        resp = order.track_order(999999999)
        assert 400 <= resp.status_code < 500

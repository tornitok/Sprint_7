from http import HTTPStatus
import allure

from api.endpoint.order import Order
from config import URL
from utils.order_generator import create_order_and_get_id


@allure.feature("Orders")
@allure.story("Accept order")
@allure.title("Courier can accept existing order and receives ok=true")
def test_accept_order_success_returns_ok_true(create_session, courier):
    order = Order(session=create_session, endpoint=URL.BASE_URL)
    with allure.step("Create an order and retrieve order_id"):
        order_id = create_order_and_get_id(order, ["BLACK"])

    with allure.step("Register and login courier to get courier_id"):
        assert courier.post_user().status_code == HTTPStatus.CREATED
        login_resp = courier.post_login_users(
            {"login": courier.user_data["login"], "password": courier.user_data["password"]}
        )
        assert login_resp.status_code == HTTPStatus.OK
        courier_id = login_resp.json()["id"]

    with allure.step("Accept order by courier"):
        resp = order.accept_order(order_id, courier_id)
        assert resp.status_code == HTTPStatus.OK
        assert resp.json().get("ok") is True


@allure.feature("Orders")
@allure.story("Accept order")
@allure.title("Accepting an order without courier id returns client error")
def test_accept_order_without_courier_id_returns_error(create_session):
    order = Order(session=create_session, endpoint=URL.BASE_URL)
    with allure.step("Create an order and retrieve order_id"):
        order_id = create_order_and_get_id(order, ["BLACK"])

    with allure.step("Call accept without courierId param"):
        resp = order.accept_order_without_courier(order_id)
        assert 400 <= resp.status_code < 500


@allure.feature("Orders")
@allure.story("Accept order")
@allure.title("Accept with invalid courier id returns client error")
def test_accept_order_with_invalid_courier_id_returns_error(create_session):
    order = Order(session=create_session, endpoint=URL.BASE_URL)
    with allure.step("Create an order and retrieve order_id"):
        order_id = create_order_and_get_id(order, ["BLACK"])

    with allure.step("Accept order with clearly invalid courier id"):
        resp = order.accept_order(order_id, courier_id=999999999)
        assert 400 <= resp.status_code < 500


@allure.feature("Orders")
@allure.story("Accept order")
@allure.title("Accept without order id in path returns client error")
def test_accept_order_without_order_id_returns_error(create_session, courier):
    order = Order(session=create_session, endpoint=URL.BASE_URL)

    with allure.step("Register and login courier to get courier_id"):
        assert courier.post_user().status_code == HTTPStatus.CREATED
        login_resp = courier.post_login_users(
            {"login": courier.user_data["login"], "password": courier.user_data["password"]}
        )
        assert login_resp.status_code == HTTPStatus.OK
        courier_id = login_resp.json()["id"]

    with allure.step("Call accept endpoint without order id segment"):
        resp = order.accept_order_without_order_id(courier_id)
        assert 400 <= resp.status_code < 500


@allure.feature("Orders")
@allure.story("Accept order")
@allure.title("Accept with invalid order id returns client error")
def test_accept_order_with_invalid_order_id_returns_error(create_session, courier):
    order = Order(session=create_session, endpoint=URL.BASE_URL)

    with allure.step("Register and login courier to get courier_id"):
        assert courier.post_user().status_code == HTTPStatus.CREATED
        login_resp = courier.post_login_users(
            {"login": courier.user_data["login"], "password": courier.user_data["password"]}
        )
        assert login_resp.status_code == HTTPStatus.OK
        courier_id = login_resp.json()["id"]

    with allure.step("Attempt to accept clearly invalid order id"):
        resp = order.accept_order(order_id=999999999, courier_id=courier_id)
        assert 400 <= resp.status_code < 500

from http import HTTPStatus
import pytest
import allure


@allure.feature("Orders")
@allure.story("Create order")
@allure.title("Creating order with different color combinations returns track")
@pytest.mark.parametrize(
    "colors",
    [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None,
    ],
)
def test_create_order_with_colors_returns_track(order_client, colors):
    with allure.step(f"Prepare client and payload with colors={colors}"):
        client = order_client(colors)
    with allure.step("Create order and validate track is returned"):
        resp = client.post_order()
        assert resp.status_code == HTTPStatus.CREATED
        body = resp.json()
        assert "track" in body and isinstance(body["track"], int)


@allure.feature("Orders")
@allure.story("Orders list")
@allure.title("Fetching orders list returns list of orders")
@pytest.mark.usefixtures("order_api")
def test_orders_list_returns_list(order_api):
    with allure.step("Request list of orders"):
        resp = order_api.get_orders_list()
    with allure.step("Validate 200 and 'orders' is a list"):
        assert resp.status_code == HTTPStatus.OK
        body = resp.json()
        assert "orders" in body and isinstance(body["orders"], list)

from http import HTTPStatus
import allure


@allure.feature("Courier")
@allure.story("Delete courier")
@allure.title("Deleting an existing courier returns ok=true")
def test_delete_courier_success_returns_ok_true(courier):
    with allure.step("Create courier"):
        create_resp = courier.post_user()
        assert create_resp.status_code == HTTPStatus.CREATED

    with allure.step("Login to get courier id"):
        login_payload = {
            'login': courier.user_data['login'],
            'password': courier.user_data['password'],
        }
        login_resp = courier.post_login_users(login_payload)
        assert login_resp.status_code == HTTPStatus.OK
        courier_id = login_resp.json()['id']

    with allure.step("Delete courier by id"):
        delete_resp = courier.delete_user(courier_id)
        assert delete_resp.status_code == HTTPStatus.OK
        assert delete_resp.json().get('ok') is True


@allure.feature("Courier")
@allure.story("Delete courier")
@allure.title("Deleting without id returns client error")
def test_delete_courier_without_id_returns_error(courier):
    with allure.step("Call delete endpoint without id path segment"):
        resp = courier.delete_user_without_id()
        assert 400 <= resp.status_code < 500


@allure.feature("Courier")
@allure.story("Delete courier")
@allure.title("Deleting non-existent courier returns 404")
def test_delete_non_existent_courier_returns_404(courier):
    with allure.step("Attempt to delete clearly non-existent id"):
        resp = courier.delete_user(999999999)
        assert resp.status_code == HTTPStatus.NOT_FOUND


@allure.feature("Courier")
@allure.story("Delete courier")
@allure.title("Deleting same courier twice returns 404 on second attempt")
def test_delete_courier_twice_returns_error(courier):
    with allure.step("Create courier"):
        create_resp = courier.post_user()
        assert create_resp.status_code == HTTPStatus.CREATED

    with allure.step("Login to get courier id"):
        login_payload = {
            'login': courier.user_data['login'],
            'password': courier.user_data['password'],
        }
        login_resp = courier.post_login_users(login_payload)
        assert login_resp.status_code == HTTPStatus.OK
        courier_id = login_resp.json()['id']

    with allure.step("Delete courier first time"):
        first_delete = courier.delete_user(courier_id)
        assert first_delete.status_code == HTTPStatus.OK

    with allure.step("Delete courier second time - expect 404"):
        second_delete = courier.delete_user(courier_id)
        assert second_delete.status_code == HTTPStatus.NOT_FOUND

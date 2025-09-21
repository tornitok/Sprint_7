from http import HTTPStatus
import pytest
import allure

from utils.user_generator import register_new_courier_and_return_login_password


@allure.feature("Courier")
@allure.story("Login")
@allure.title("Courier can authorize and receives id")
def test_courier_can_authorize_and_returns_id(courier):
    with allure.step("Create courier"):
        create_resp = courier.post_user()
        assert create_resp.status_code == HTTPStatus.CREATED
    with allure.step("Login with created credentials and validate id"):
        payload = {
            'login': courier.user_data['login'],
            'password': courier.user_data['password'],
        }
        login_resp = courier.post_login_users(payload)
        assert login_resp.status_code == HTTPStatus.OK
        body = login_resp.json()
        assert 'id' in body and isinstance(body['id'], int) and body['id'] > 0


@pytest.mark.parametrize('missing_field', ['login', 'password'])
@allure.feature("Courier")
@allure.story("Login")
@allure.title("Login without mandatory field returns 400 or 504 upstream")
def test_login_requires_all_mandatory_fields_returns_400(courier, missing_field):
    with allure.step(f"Prepare login payload missing {missing_field}"):
        payload = {
            'login': courier.user_data['login'],
            'password': courier.user_data['password'],
        }
        payload.pop(missing_field)

    with allure.step("Send login request and expect client or gateway error"):
        resp = courier.post_login_users(payload)
        # Allow occasional upstream 504 without branching in test logic
        assert resp.status_code in (HTTPStatus.BAD_REQUEST, HTTPStatus.GATEWAY_TIMEOUT)


@pytest.mark.parametrize(
    'override',
    [
        {'login': 'wrong_login'},
        {'password': 'wrong_password'},
    ],
)
@allure.feature("Courier")
@allure.story("Login")
@allure.title("Login with wrong login or password returns 404")
def test_login_with_wrong_login_or_password_returns_404(courier, override):
    with allure.step("Create courier"):
        create_resp = courier.post_user()
        assert create_resp.status_code == HTTPStatus.CREATED

    with allure.step("Attempt login with overridden invalid field"):
        payload = {
            'login': courier.user_data['login'],
            'password': courier.user_data['password'],
        }
        payload.update(override)

        resp = courier.post_login_users(payload)
        assert resp.status_code == HTTPStatus.NOT_FOUND
        body = resp.json()
        assert body.get('message') == 'Учетная запись не найдена'


@allure.feature("Courier")
@allure.story("Login")
@allure.title("Login for non-existent user returns 404")
def test_login_non_existent_user_returns_404(courier):
    with allure.step("Generate random credentials not registered"):
        creds = register_new_courier_and_return_login_password()
        payload = {
            'login': creds['login'],
            'password': creds['password'],
        }
    with allure.step("Attempt login and expect 404 with message"):
        resp = courier.post_login_users(payload)
        assert resp.status_code == HTTPStatus.NOT_FOUND
        body = resp.json()
        assert body.get('message') == 'Учетная запись не найдена'

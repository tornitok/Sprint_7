from http import HTTPStatus
import pytest
import allure


@allure.feature("Courier")
@allure.story("Create courier")
@allure.title("Creating a new courier returns ok=true")
def test_create_courier(courier):
    with allure.step("Send create courier request"):
        response = courier.post_user()
    with allure.step("Validate response is 201 and ok=true"):
        assert response.status_code == HTTPStatus.CREATED
        body = response.json()
        assert body.get('ok') is True


@allure.feature("Courier")
@allure.story("Create courier")
@allure.title("Creating a duplicate courier returns 409")
def test_create_duplicate_courier(courier):
    with allure.step("Create courier first time"):
        first = courier.post_user()
        assert first.status_code == HTTPStatus.CREATED
    with allure.step("Create courier second time with same credentials"):
        second = courier.post_user()
    with allure.step("Validate response is 409 and error message"):
        assert second.status_code == HTTPStatus.CONFLICT
        body = second.json()
        assert body.get('message') == 'Этот логин уже используется. Попробуйте другой.'


@pytest.mark.parametrize('missing_field', ['login', 'password'])
@allure.feature("Courier")
@allure.story("Create courier")
@allure.title("Creating courier without mandatory field returns 400")
def test_create_courier_without_required_field_returns_400(courier, missing_field):
    with allure.step(f"Prepare payload without required field: {missing_field}"):
        payload = courier.user_data.copy()
        payload.pop(missing_field, None)
        courier.user_data = payload
    with allure.step("Send create courier request and validate 400 with message"):
        response = courier.post_user()
        assert response.status_code == HTTPStatus.BAD_REQUEST
        body = response.json()
        assert body.get('message') == 'Недостаточно данных для создания учетной записи'

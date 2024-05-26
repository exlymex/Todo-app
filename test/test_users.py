from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user/get-user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithrobytest'
    assert response.json()['email'] == 'test@test.test'
    assert response.json()['role'] == 'admin'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['phone_number'] == '(111)-111-1111'


def test_change_password_success(test_user):
    response = client.put("/user/change-password", json={"new_password": "123123123"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_phone_number_success(test_user):
    response = client.put("/user/change-phone", json={"phone_number": "(111)-111-1111"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

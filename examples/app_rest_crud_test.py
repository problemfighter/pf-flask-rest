import json
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/person/"


def test__invalid_post_json():
    data = {'last_name': "com", 'email': 'hmtmcse.com', 'age': 7, 'income': 5000}
    headers = {'Content-type': 'application/json'}

    response = requests.post(BASE_URL + "create", data=json.dumps(data), headers=headers)
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data["status"] == "error", "Should be error"


def test__post_json_validation_error():
    data = {
        "data": {'last_name': "com", 'email': 'hmtmcse.com', 'age': 7, 'income': 5000}
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(BASE_URL + "create", data=json.dumps(data), headers=headers)
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data["status"] == "error", "Should be error"


def test__post_json_create():
    data = {
        "data": {'first_name': 'hmtmcse', 'last_name': "com", 'email': 'hmtmcse.com@gmail.com', 'age': 7, 'income': 5000}
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(BASE_URL + "create", data=json.dumps(data), headers=headers)
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"


def test__post_json_details_response_create():
    first_name = 'hmtmcse'
    data = {
        "data": {'first_name': first_name, 'last_name': "com", 'email': 'hmtmcse.com@gmail.com', 'age': 7, 'income': 5000}
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(BASE_URL + "details-response-create", data=json.dumps(data), headers=headers)
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"
    assert response_data['data']['first_name'] == first_name, "Should be " + first_name


def test__get_list():
    response = requests.get(BASE_URL + "list")
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert "pagination" in response_data, "Should be pagination"
    assert "data" in response_data, "Should be data"


def test__get_list_pagination():
    response = requests.get(BASE_URL + "list?per-page=2&sort-order=asc")
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert "pagination" in response_data, "Should be pagination"
    assert "data" in response_data, "Should be data"
    assert response_data["pagination"]['itemPerPage'] == 2, "Should be 2"
    assert response_data["data"][0]['id'] == 1, "Should be 1"


def test__post_json_update():
    data = {
        "data": {
            'id': 1,
            'first_name': 'Touhid',
            'last_name': "Mia",
            'email': 'hmtmcse.com@gmail.com',
            'age': 7,
            'income': 1000
        }
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(BASE_URL + "update", data=json.dumps(data), headers=headers)
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"


def test__details():
    response = requests.get(BASE_URL + "details/1")
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert "data" in response_data, "Should be data"


def test__delete():
    response = requests.delete(BASE_URL + "delete/1")
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"


def test__restore():
    response = requests.get(BASE_URL + "restore/1")
    response_data = response.json()
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"


if __name__ == '__main__':
    test__invalid_post_json()
    test__post_json_validation_error()
    test__post_json_create()
    test__post_json_details_response_create()
    test__get_list()
    test__get_list_pagination()
    test__post_json_update()
    test__details()
    test__delete()
    test__restore()


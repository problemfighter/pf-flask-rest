import json
import requests

BASE_URL = "http://127.0.0.1:5000//api/v1/person/"


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
    response_data = json.loads(response.json())
    assert response.status_code == 200, "Should be 200"
    assert response_data['status'] == "success", "Should be success"


if __name__ == '__main__':
    test__invalid_post_json()
    test__post_json_validation_error()
    test__post_json_create()


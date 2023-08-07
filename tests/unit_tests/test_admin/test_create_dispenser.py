from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from core.constants import SUCCESS_MESSAGE


def test_create_dispenser_success(client: TestClient):
    """
    Test successful creation of a new dispenser:
    :param client: A TestClient instance to simulate HTTP requests.
    :return: None
    """
    request_data = {"flow_volume": "10.5", "price": 25.99}
    response = client.post("/dispensers", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "data" in response.json()
    assert "message" in response.json()
    assert response.json()["data"]["flow_volume"] == request_data["flow_volume"]
    assert response.json()["data"]["price"] == request_data["price"]
    assert response.json()["message"] == SUCCESS_MESSAGE


def test_create_dispenser_missing_data(client: TestClient):
    """
    Test failure to create a new dispenser due to missing data:
    :param client: A TestClient instance to simulate HTTP requests.
    :return: None
    """
    request_data = {"flow_volume": "10.5"}
    response = client.post("/dispensers", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
    assert "price" in response.json()["detail"][0]["loc"]


def test_create_dispenser_invalid_data(client: TestClient):
    """
    Test failure to create a new dispenser due to invalid data:
    :param client: A TestClient instance to simulate HTTP requests.
    :return: None
    """
    request_data = {"flow_volume": "abc", "price": "xyz"}
    response = client.post("/dispensers", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
    assert "flow_volume" in response.json()["detail"][0]["loc"] or "price" in response.json()["detail"][0]["loc"]


def test_create_dispenser_db_error(client: TestClient):
    """
    Test failure to create a new dispenser due to database error:
    :param client: A TestClient instance to simulate HTTP requests.
    :return: None
    """
    request_data = {"flow_volume": "10.5", "price": 25.99}
    with patch("apps.admin.routes.add_dispenser") as mock_add_dispenser:
        mock_add_dispenser.return_value = {"message": "Database error", "data": None}
        response = client.post("/dispensers", json=request_data)
    assert "message" in response.json()
    assert "Database error" in response.json()["message"]


def test_create_dispenser_unexpected_error(client: TestClient):
    """
    Test failure to create a new dispenser due to unexpected error:
    :param client: A TestClient instance to simulate HTTP requests.
    :return: None
    """
    request_data = {"flow_volume": "10.5", "price": 25.99}
    with patch("apps.admin.routes.add_dispenser") as mock_add_dispenser:
        mock_add_dispenser.return_value = {"message": "Unexpected error", "data": None}
        response = client.post("/dispensers", json=request_data)
    assert "message" in response.json()
    assert "Unexpected error" in response.json()["message"]

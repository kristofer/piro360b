import requests
from rest import Piro360rest


def test_read():
    client = requests.Session()
    response = client.get("http://localhost:8000/")
    print("Test", response.json())

def test_read_root():
    client = requests.Session()
    response = client.get("http://localhost:8000/")
    print("Test", response.json())

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Piro360 REST server"}


def test_read_root_fail():
    client = requests.Session()
    response = client.get("http://localhost:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome --- server"}

def test_read_item():
    client = requests.Session()
    response = client.get("http://localhost:8000/items/1?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "test"}


if __name__ == "__main__":
    test_read()
    test_read_root()
    test_read_root_fail()
    test_read_item()
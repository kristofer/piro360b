import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Piro, Tag, User
from rest import Piro360rest

# Create a new SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a TestClient
app_instance = Piro360rest(TestingSessionLocal)
client = TestClient(app_instance.start())

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(db):
    response = client.post("/users/", json={"email": "test@example.com", "firstname": "Test", "lastname": "User"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["firstname"] == "Test"
    assert data["lastname"] == "User"

def test_read_users(db):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_piro(db):
    user = User(email="test@example.com", firstname="Test", lastname="User")
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/piros/", json={"title": "Test Piro", "description": "This is a test piro", "s3urltovideo": "http://s3.com/video", "imagename": "image.jpg", "location": "Test Location", "created": "2021-01-01", "owner_id": user.id})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Piro"
    assert data["description"] == "This is a test piro"

def test_read_piros(db):
    response = client.get("/piros/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_tag(db):
    user = User(email="test@example.com", firstname="Test", lastname="User")
    db.add(user)
    db.commit()
    db.refresh(user)
    response = client.post("/tags/", json={"title": "Test Tag", "description": "This is a test tag", "owner_id": user.id})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Tag"
    assert data["description"] == "This is a test tag"

def test_read_tags(db):
    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

if __name__ == "__main__":
    test_create_user(TestingSessionLocal())
    test_read_users()
    test_create_piro()
    test_read_piros()
    test_create_tag()
    test_read_tags()
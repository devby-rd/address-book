import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# The setup_database fixture will create the database tables before each test and drop them after the tests are done
@pytest.fixture(autouse=True)
def setup_database():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database tables after tests are done
    Base.metadata.drop_all(bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the get_db dependency in the app
app.dependency_overrides[get_db] = override_get_db

# Create a TestClient for testing the API endpoints
client = TestClient(app)


def create_sample_address_payload():
    response = client.post("/addresses/", json={
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "email": "john.doe@example.com",
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345",
    "country": "USA",
    "latitude": 37.7749,
    "longitude": -122.4194
    })
    return response


def test_create_address():
    response = create_sample_address_payload()

    # Assert that the response status code is 200 (OK) and that the response data contains the expected values
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["latitude"] == 37.7749
    assert data["longitude"] == -122.4194
    assert "id" in data
    assert "created_at" in data


def test_update_address():
    response = create_sample_address_payload()
    assert response.status_code == 200
    address_id = response.json()["id"]
    
    # update the address using its ID and assert that the response status code is 200 (OK) and that the response data contains the updated values
    response = client.put(f"/addresses/{address_id}", json={
        "first_name": "Jane",
        "last_name": "Smith",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["latitude"] == 37.7749  # latitude should remain unchanged
    assert data["longitude"] == -122.4194  # longitude should remain unchanged


def test_get_address():
    response = create_sample_address_payload()
    assert response.status_code == 200
    address_id = response.json()["id"]

    # get the address using its ID and that the response data contains the expected values
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"
    assert response.json()["latitude"] == 37.7749
    assert response.json()["longitude"] == -122.4194


def test_get_addresses():
    response = create_sample_address_payload()
    assert response.status_code == 200
    
    # get all addresses and that the response data contains a list with the expected address
    response = client.get("/addresses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "John"
    assert data[0]["last_name"] == "Doe"
    assert data[0]["latitude"] == 37.7749
    assert data[0]["longitude"] == -122.4194


def test_nearby_addresses():
    response = create_sample_address_payload()
    assert response.status_code == 200

    # get nearby addresses within a radius of 10 km from the coordinates of the address we created and that the response data contains a list with the expected address
    response = client.get("/addresses/nearby/?latitude=37.7749&longitude=-122.4194&radius=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "John"
    assert data[0]["last_name"] == "Doe"
    assert data[0]["latitude"] == 37.7749
    assert data[0]["longitude"] == -122.4194


def test_delete_address():
    response = create_sample_address_payload()
    assert response.status_code == 200
    address_id = response.json()["id"]

    # delete the address using its ID and that the response data contains the expected values
    response = client.delete(f"/addresses/{address_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["latitude"] == 37.7749
    assert data["longitude"] == -122.4194

    # after deleting the address, we should get a 404 error when we try to get it again using its ID
    response = client.get(f"/addresses/{address_id}")
    assert response.status_code == 404

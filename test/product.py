from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_item():
    response = client.post(
        "/product/",
        json={"title": "Foo Bar", "description": "The Foo Barters", "stocks": 12},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "product created"
    }


def test_get_list_product():
    response = client.get("/product")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Foo Bar"
    assert data[0]["description"] == "The Foo Barters"
    assert data[0]["stocks"] == 12


def test_get_product():
    response = client.get("/product/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Foo Bar"
    assert data["description"] == "The Foo Barters"
    assert data["stocks"] == 12


def test_update_product():
    response = client.put(
        "/product/1",
        json={"title": "Foo Bar", "description": "has changed", "stocks": 12},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "product updated"
    }

    response = client.get("/product/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Foo Bar"
    assert data["description"] == "has changed"
    assert data["stocks"] == 12


def test_get_bad_product():
    response = client.get("/product/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }

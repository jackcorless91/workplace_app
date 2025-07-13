import pytest
from app import create_app
from init import db as _db
import os


@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "testing"
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    app = create_app()
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Optional: in-memory DB
    with app.test_client() as client:
        yield client
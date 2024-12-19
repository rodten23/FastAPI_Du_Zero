import pytest
from fastapi.testclient import TestClient

from fastapi_du_zero.app import app


@pytest.fixture()  # Arrange (Organização)
def client():
    return TestClient(app)

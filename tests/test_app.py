from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_du_zero.app import app


def test_read_root_deve_retonar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (Organização)

    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olá, Mundo!'}  # Assert (Afirmação)

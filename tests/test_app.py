from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_du_zero.app import app


def test_read_root_deve_retonar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (Organização)

    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olá, Mundo!'}  # Assert (Afirmação)


def test_create_user_retornar_created_e_nome_email_id():
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'melissa',
            'email': 'melissa@exemplo.com',
            'password': 'segredo',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@exemplo.com',
        'id': 1,
    }

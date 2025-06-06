from http import HTTPStatus

from fastapi_du_zero.schemas import UserPublic


def test_read_root_deve_retonar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olá, Mundo!'}  # Assert (Afirmação)


def test_html_page_deve_retonar_a_pagina_html(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
        <html>
            <head>
                <title>Página do Olá, Mundo!</title>
            </head>
            <body>
                <h1>Chega mais, Mundão!</h1>
            </body>
        </html>"""
    )


def test_create_user_retornar_created_e_nome_email_id(client):
    response = client.post(
        '/users',
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


def test_read_users_retornar_ok_e_lista_vazia(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_retornar_ok_e_lista_nome_email_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_cenario_feliz_OK_e_retorna_nome_email_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@exemplo.com',
        'id': 1,
    }


def test_get_user_cenario_erro_not_found_e_usuario_nao_encontrado(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_update_user_cenario_feliz_OK_e_retorna_nome_email_id(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'melissa',
            'email': 'melissa@exemplo.com',
            'password': 'novo-segredo',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@exemplo.com',
        'id': 1,
    }


def test_update_user_cenario_erro_not_found_e_usuario_nao_encontrado(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'melissa',
            'email': 'melissa@exemplo.com',
            'password': 'novo-segredo',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_delete_user_cenario_feliz_OK_e_retorna_usuario_excluido(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuário excluído!'}


def test_delete_user_cenario_erro_not_found_e_usuario_nao_encontrado(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}

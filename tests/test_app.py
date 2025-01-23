from http import HTTPStatus


def test_read_root_deve_retonar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olá, Mundo!'}  # Assert (Afirmação)


def test_create_user_retornar_created_e_nome_email_id(client):
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
        'id': 1
    }


def test_read_users_retornar_ok_e_lista_nome_email_id(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users':
        [
            {
                'username': 'melissa',
                'email': 'melissa@exemplo.com',
                'id': 1
            }
        ]
    }


def test_update_users_cenario_feliz_OK_e_retorna_nome_email_id(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'melissa',
            'email': 'melissa@exemplo.com',
            'password': 'novo-segredo'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'melissa',
        'email': 'melissa@exemplo.com',
        'id': 1
    }


def test_update_users_cenario_erro_not_found_e_usuario_nao_encontrado(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'melissa',
            'email': 'melissa@exemplo.com',
            'password': 'novo-segredo'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado!'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'Usuário excluído!'}

from fastapi_du_zero.models import User


def test_create_user(client):
    user = User(username = 'Rodrigo', email = 'rodrigo@encadernacao.com', password = 'vamosla')

    assert user.password == 'vamosla'
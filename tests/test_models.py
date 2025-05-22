from dataclasses import asdict

from sqlalchemy import select

from fastapi_du_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Rodrigo',
            email='rodrigo@encadernacao.com.br',
            password='vamosla',
        )

        session.add(new_user)
        session.commit()

    result = session.scalar(
        select(User).where(User.email == 'rodrigo@encadernacao.com.br')
    )

    assert asdict(result) == {
        'id': 1,
        'username': 'Rodrigo',
        'password': 'vamosla',
        'email': 'rodrigo@encadernacao.com.br',
        'created_at': time[0],
        'updated_at': time[1]
    }

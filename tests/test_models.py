from sqlalchemy import select

from fastapi_du_zero.models import User


def test_create_user(session):
    user = User(
        username='Rodrigo',
        email='rodrigo@encadernacao.com',
        password='vamosla',
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'rodrigo@encadernacao.com')
    )

    assert result.username == 'Rodrigo'

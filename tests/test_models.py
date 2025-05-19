from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from fastapi_du_zero.models import User, table_registry


def test_create_user():
    # Cria o banco de dados temporário em memória para o teste.
    # O parâmetro :memory: não funciona para todos os tipos de DB.
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
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

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_du_zero.app import app
from fastapi_du_zero.database import get_session
from fastapi_du_zero.models import User, table_registry

# pytest.fixture é um bloco de teste reutilizável do Pytest.


@pytest.fixture  # Arrange (Organização)
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Cria o banco de dados temporário em memória para o teste.
    # O parâmetro :memory: não funciona para todos os tipos de DB.
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    # Até aqui é o Arrange do teste.
    # E o drop.all abaixo é o "Tear down" do teste.
    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(
    *,
    model,
    time_created_at=datetime(2025, 5, 20),
    time_updated_at=datetime(2025, 5, 21),
):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time_created_at
        if hasattr(target, 'updated_at'):
            target.updated_at = time_updated_at

    event.listen(model, 'before_insert', fake_time_hook)

    yield time_created_at, time_updated_at

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    user = User(
        username='Teste',
        email='teste@teste.com',
        password='senha-teste')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

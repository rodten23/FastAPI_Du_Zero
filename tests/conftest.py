import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_du_zero.app import app
from fastapi_du_zero.models import table_registry

# pytest.fixture é um bloco de teste reutilizável do Pytest.


@pytest.fixture  # Arrange (Organização)
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Cria o banco de dados temporário em memória para o teste.
    # O parâmetro :memory: não funciona para todos os tipos de DB.
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    # Até aqui é o Arrange do teste.
    # E o drop.all abaixo é o "Tear down" do teste.
    table_registry.metadata.drop_all(engine)

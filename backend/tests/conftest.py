import pytest
from sqlalchemy.orm import Session
from app.db.session import engine
from fastapi.testclient import TestClient

from app.api.deps import get_db
from app.main import app
   
"""
 un pytest fixture, es una función especial que se utiliza para preparar y configurar el entorno,
 los datos o los recursos que un test necesita antes de ejecutarse, en eset caso es la sesion que entra a nuestra 
 base de datos de prueba

"""

@pytest.fixture
def db_session():
    with engine.connect() as connection:
        transaction = connection.begin()

        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        ) as session:
            try:
                yield session
            finally:
                session.close()
                transaction.rollback()

"""
Hacemos un segundo fixture donde indicamos a fastapi que en el periodo de pruebas , en vez de usar la conexion 
get_db, use la adecuada para la prueba 

"""
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)  
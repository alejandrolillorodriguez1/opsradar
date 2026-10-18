from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings


resettings = get_settings()

db_url = URL.create(
    drivername="postgresql+psycopg",    
    username=resettings.db_user,
    password=resettings.db_password.get_secret_value(),
    host=resettings.db_host,
    port=resettings.db_port,
    database=resettings.db_name,
)

engine = create_engine(db_url,pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





"""
Este archivo prepara el acceso de la aplicación a PostgreSQL.

1.  get_settings() obtiene los datos de conexión que hemos definido
    en la configuración: servidor, puerto, usuario, contraseña y base de datos.

2.  URL.create() reúne esos datos en una dirección de conexión.
    Indicamos postgresql+psycopg porque usamos PostgreSQL con Psycopg 3.

3.  engine gestiona las conexiones con PostgreSQL.

4.  SessionLocal utiliza esas conexiones para consultar, añadir, modificar 
    o eliminar datos, y confirmar o deshacer cambios.Como configuramos SessionLocal con bind=engine, 
    cada sesión que creamos ya sabe qué motor utilizar.
    Cuando necesita consultar o guardar datos, obtiene automáticamente una conexión del engine

Este archivo solo prepara estas herramientas.
No ejecuta consultas, no crea tablas y no abre una sesión todavía.
La primera conexión real se abrirá cuando necesitemos utilizarla.
"""
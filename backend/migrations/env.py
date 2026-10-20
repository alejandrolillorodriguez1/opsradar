from app.models.organization import Organization
from app.db.base import Base
from app.db.session import engine
from alembic import context

config = context.config
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

def run_migrations_online() -> None:
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


    """
Este archivo configura cómo Alembic utiliza nuestras migraciones.

Alembic permite generar archivos con cambios en las tablas y aplicarlos
a PostgreSQL. Aquí le indicamos cómo conectarse y dónde encontrar
la descripción de nuestras tablas.

Tiene dos modos de trabajo:

- Online: conecta con PostgreSQL y ejecuta los cambios.
  Es el modo que utilizaremos normalmente.

- Offline: genera las instrucciones SQL sin conectarse a PostgreSQL.
  Sirve para revisarlas o ejecutarlas por otro procedimiento.
  No significa trabajar sin internet, sino sin conexión a la base de datos.

No tenemos que escribir dos versiones de cada migración.
Los dos modos utilizan los mismos archivos de cambios.

Base.metadata reúne la descripción de los modelos que hemos importado.
Alembic la compara con la base de datos al generar una migración automática.
Por eso importamos Organization aunque no usemos su nombre directamente.

Las migraciones generadas deben revisarse antes de aplicarlas.
Generar el archivo no significa que los cambios ya estén aplicados.
"""

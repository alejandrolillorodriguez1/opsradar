from sqlalchemy import DeclarativeBase

class Base(DeclarativeBase):
    pass


"""
Define la base común de nuestros modelos. 
Permite reunir la descripción de las tablas para que Alembic pueda compararlas con la base de datos 
y preparar los cambios.

"""
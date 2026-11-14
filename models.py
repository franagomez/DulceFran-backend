"""
Modelos de base de datos (tablas), usando SQLAlchemy ORM.
Los nombres de los campos son exactamente los mismos que ya usa el frontend
en src/data/productos.js, usuarios.js y pedidos.js, para que la integración
después sea directa (no hay que renombrar nada en React).
"""
from sqlalchemy import Column, Integer, String, Float
from database import Base


class Producto(Base):
    __tablename__ = "productos"

    codigo = Column(String, primary_key=True, index=True)
    categoria = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    stockCritico = Column(Integer, nullable=False, default=0)


class Usuario(Base):
    __tablename__ = "usuarios"

    correo = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    # Guardamos el hash de la contraseña, nunca la contraseña en texto plano.
    contrasenaHash = Column(String, nullable=False)
    telefono = Column(String, nullable=True, default="")
    region = Column(String, nullable=True)
    comuna = Column(String, nullable=True)
    rol = Column(String, nullable=False, default="Cliente")  # Administrador | Vendedor | Cliente


class MensajeContacto(Base):
    __tablename__ = "mensajes_contacto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    comentario = Column(String, nullable=False)
    fecha = Column(String, nullable=False)

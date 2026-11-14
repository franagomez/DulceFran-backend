"""
Esquemas de Pydantic: definen qué forma tiene la información que entra
(peticiones) y sale (respuestas) de la API. FastAPI los usa para validar
automáticamente y para generar la documentación de Swagger.
"""
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# ---------- Productos ----------

class ProductoBase(BaseModel):
    categoria: str
    nombre: str
    precio: int
    descripcion: Optional[str] = ""
    stock: int = 0
    stockCritico: int = 0


class ProductoCrear(ProductoBase):
    codigo: str


class ProductoActualizar(BaseModel):
    categoria: Optional[str] = None
    nombre: Optional[str] = None
    precio: Optional[int] = None
    descripcion: Optional[str] = None
    stock: Optional[int] = None
    stockCritico: Optional[int] = None


class ProductoRespuesta(ProductoBase):
    codigo: str
    model_config = ConfigDict(from_attributes=True)


# ---------- Usuarios ----------

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: Optional[str] = ""
    region: Optional[str] = None
    comuna: Optional[str] = None


class UsuarioCrear(UsuarioBase):
    contrasena: str
    rol: str = "Cliente"


class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    contrasena: Optional[str] = None
    telefono: Optional[str] = None
    region: Optional[str] = None
    comuna: Optional[str] = None
    rol: Optional[str] = None


class UsuarioRespuesta(UsuarioBase):
    rol: str
    model_config = ConfigDict(from_attributes=True)


# ---------- Autenticación ----------

class LoginDatos(BaseModel):
    correo: EmailStr
    contrasena: str


class TokenRespuesta(BaseModel):
    token: str
    usuario: UsuarioRespuesta


# ---------- Mensajes de contacto ----------

class MensajeCrear(BaseModel):
    nombre: str
    correo: EmailStr
    comentario: str


class MensajeRespuesta(MensajeCrear):
    id: int
    fecha: str
    model_config = ConfigDict(from_attributes=True)

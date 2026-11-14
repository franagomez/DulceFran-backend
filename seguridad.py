"""
Funciones de seguridad: hash de contraseñas y manejo del JWT.

Flujo (el mismo que explica el PDF de la clase):
1. Login: se valida correo+contraseña contra la base de datos y, si son
   correctos, se genera y firma un JWT con crear_token().
2. El frontend guarda ese token (localStorage/sessionStorage) y lo manda en
   cada petición protegida como: Authorization: Bearer <token>
3. Cada ruta protegida usa obtener_usuario_actual (o requiere_rol) como
   dependencia: FastAPI valida el token automáticamente antes de ejecutar
   la función de la ruta. Si el token no viene, está vencido o es inválido,
   responde 401 solo.
"""
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

# En un proyecto real esta clave NO se deja en el código: se lee desde una
# variable de entorno. Para el parcial la dejamos aquí para simplificar.
CLAVE_SECRETA = "dulcefran-clave-secreta-parcial3-cambiar-en-produccion"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
seguridad_bearer = HTTPBearer()


def hashear_contrasena(contrasena: str) -> str:
    return pwd_context.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hash)


def crear_token(correo: str, rol: str, nombre: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    payload = {"sub": correo, "rol": rol, "nombre": nombre, "exp": expira}
    return jwt.encode(payload, CLAVE_SECRETA, algorithm=ALGORITMO)


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad_bearer),
) -> dict:
    """Dependencia que valida el JWT recibido en el header Authorization.
    Si es válido, devuelve su contenido (correo, rol, nombre). Si no, 401."""
    token = credenciales.credentials
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return payload


def requiere_rol(*roles_permitidos: str):
    """Fábrica de dependencias: requiere_rol("Administrador", "Vendedor")
    deja pasar solo a esos roles; a cualquier otro le responde 403."""

    def verificador(usuario: dict = Depends(obtener_usuario_actual)) -> dict:
        if usuario.get("rol") not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para realizar esta acción",
            )
        return usuario

    return verificador

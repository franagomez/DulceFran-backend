"""Rutas de autenticación: login y registro de clientas/clientes nuevos."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import obtener_db
from seguridad import crear_token, hashear_contrasena, verificar_contrasena

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=schemas.TokenRespuesta)
def login(datos: schemas.LoginDatos, db: Session = Depends(obtener_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == datos.correo).first()

    if not usuario or not verificar_contrasena(datos.contrasena, usuario.contrasenaHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    token = crear_token(correo=usuario.correo, rol=usuario.rol, nombre=usuario.nombre)
    return {"token": token, "usuario": usuario}


@router.post("/registro", response_model=schemas.UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registro(datos: schemas.UsuarioCrear, db: Session = Depends(obtener_db)):
    """Registro público: siempre crea la cuenta con rol Cliente,
    igual que registrarUsuario() en el frontend actual."""
    existe = db.query(models.Usuario).filter(models.Usuario.correo == datos.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta registrada con ese correo")

    nuevo = models.Usuario(
        correo=datos.correo,
        nombre=datos.nombre,
        contrasenaHash=hashear_contrasena(datos.contrasena),
        telefono=datos.telefono or "",
        region=datos.region,
        comuna=datos.comuna,
        rol="Cliente",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

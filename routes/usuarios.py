"""CRUD de usuarias/usuarios. Todo este router requiere estar logeada como
Administrador -- es el mismo panel "Usuarias" que ya existe en /admin."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import obtener_db
from seguridad import hashear_contrasena, requiere_rol

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(requiere_rol("Administrador"))],
)


@router.get("/", response_model=list[schemas.UsuarioRespuesta])
def listar_usuarios(db: Session = Depends(obtener_db)):
    return db.query(models.Usuario).all()


@router.get("/{correo}", response_model=schemas.UsuarioRespuesta)
def obtener_usuario(correo: str, db: Session = Depends(obtener_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuaria no encontrada")
    return usuario


@router.post("/", response_model=schemas.UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: schemas.UsuarioCrear, db: Session = Depends(obtener_db)):
    if db.query(models.Usuario).filter(models.Usuario.correo == datos.correo).first():
        raise HTTPException(status_code=400, detail="Ya existe una cuenta registrada con ese correo")

    usuario = models.Usuario(
        correo=datos.correo,
        nombre=datos.nombre,
        contrasenaHash=hashear_contrasena(datos.contrasena),
        telefono=datos.telefono or "",
        region=datos.region,
        comuna=datos.comuna,
        rol=datos.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.put("/{correo}", response_model=schemas.UsuarioRespuesta)
def actualizar_usuario(correo: str, datos: schemas.UsuarioActualizar, db: Session = Depends(obtener_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuaria no encontrada")

    cambios = datos.model_dump(exclude_unset=True)
    if "contrasena" in cambios:
        nueva = cambios.pop("contrasena")
        if nueva:
            usuario.contrasenaHash = hashear_contrasena(nueva)
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{correo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(correo: str, db: Session = Depends(obtener_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuaria no encontrada")
    db.delete(usuario)
    db.commit()

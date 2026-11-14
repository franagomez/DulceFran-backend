"""Mensajes de contacto. El checklist del parcial pide como mínimo
Create + Read, así que el formulario de Contacto.jsx puede quedar público
(cualquiera puede escribir), pero solo Administrador/Vendedor pueden leer
los mensajes recibidos (sería la bandeja de entrada del panel admin)."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import obtener_db
from seguridad import requiere_rol

router = APIRouter(prefix="/mensajes", tags=["Mensajes de contacto"])


@router.post("/", response_model=schemas.MensajeRespuesta, status_code=status.HTTP_201_CREATED)
def crear_mensaje(datos: schemas.MensajeCrear, db: Session = Depends(obtener_db)):
    mensaje = models.MensajeContacto(
        nombre=datos.nombre,
        correo=datos.correo,
        comentario=datos.comentario,
        fecha=datetime.now(timezone.utc).isoformat(),
    )
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje


@router.get("/", response_model=list[schemas.MensajeRespuesta])
def listar_mensajes(
    db: Session = Depends(obtener_db),
    usuario=Depends(requiere_rol("Administrador", "Vendedor")),
):
    return db.query(models.MensajeContacto).order_by(models.MensajeContacto.id.desc()).all()

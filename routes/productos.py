"""CRUD de productos. Lectura (GET) es pública -- el catálogo lo tiene que
poder ver cualquier visitante sin iniciar sesión. Crear/editar/eliminar
requiere estar logeada como Administrador o Vendedor (mismos roles que ya
pueden entrar al panel /admin en el frontend)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import obtener_db
from seguridad import requiere_rol

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[schemas.ProductoRespuesta])
def listar_productos(db: Session = Depends(obtener_db)):
    return db.query(models.Producto).all()


@router.get("/{codigo}", response_model=schemas.ProductoRespuesta)
def obtener_producto(codigo: str, db: Session = Depends(obtener_db)):
    producto = db.query(models.Producto).filter(models.Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=schemas.ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: schemas.ProductoCrear,
    db: Session = Depends(obtener_db),
    usuario=Depends(requiere_rol("Administrador", "Vendedor")),
):
    if db.query(models.Producto).filter(models.Producto.codigo == datos.codigo).first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")
    producto = models.Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.put("/{codigo}", response_model=schemas.ProductoRespuesta)
def actualizar_producto(
    codigo: str,
    datos: schemas.ProductoActualizar,
    db: Session = Depends(obtener_db),
    usuario=Depends(requiere_rol("Administrador", "Vendedor")),
):
    producto = db.query(models.Producto).filter(models.Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    codigo: str,
    db: Session = Depends(obtener_db),
    usuario=Depends(requiere_rol("Administrador", "Vendedor")),
):
    producto = db.query(models.Producto).filter(models.Producto.codigo == codigo).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()

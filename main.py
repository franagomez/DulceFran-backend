from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routes import auth, mensajes, productos, usuarios

# Crea las tablas en dulcefran.db si todavía no existen (no borra datos
# existentes en próximos arranques).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API DulceFran",
    description="API del backend de DulceFran - Parcial 3 DSY1104",
    version="1.0.0",
)

# --- CORS: permite que el frontend (Vite, puerto 5173) consuma esta API ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rutas ---
app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(usuarios.router)
app.include_router(mensajes.router)


@app.get("/")
def raiz():
    return {"mensaje": "API DulceFran funcionando. Visita /docs para ver la documentación."}

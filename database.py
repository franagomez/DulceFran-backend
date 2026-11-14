"""
Configuración de la base de datos.
Usamos SQLite porque es un solo archivo (dulcefran.db), no requiere instalar
ni configurar ningún servidor de base de datos aparte - ideal para el alcance
de este parcial. Si más adelante quieres pasar a Postgres/Supabase, solo se
cambia la variable DATABASE_URL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./dulcefran.db"

# check_same_thread=False es necesario porque FastAPI puede usar la conexión
# desde distintos hilos (threads) al atender varias peticiones.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obtener_db():
    """Dependencia de FastAPI: entrega una sesión de base de datos por cada
    petición y la cierra automáticamente al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Configurar el motor de base de datos con pool_pre_ping para reconexiones automáticas
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True
)

# Sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para herencia de modelos ORM
Base = declarative_base()

def get_db():
    """
    Inyector de dependencias para obtener la sesión de base de datos activa.
    Garantiza que la sesión se libere y cierre al finalizar el request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

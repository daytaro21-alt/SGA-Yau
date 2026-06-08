from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class ProcedureStatus(Base):
    """
    Representa el estado actual de un trámite en el flujo de gestión documental.
    Mapea a la tabla 'estados_tramite' de la base de datos.
    """
    __tablename__ = "estados_tramite"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("nombre", String(50), unique=True, nullable=False)
    description = Column("descripcion", Text, nullable=True)
    created_at = Column("creado_en", DateTime(timezone=True), server_default=func.now())

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Citizen(Base):
    """
    Representa a un ciudadano registrado en la Municipalidad de Yau.
    Mapea a la tabla 'ciudadanos' de la base de datos.
    """
    __tablename__ = "ciudadanos"

    id = Column("id", Integer, primary_key=True, index=True)
    dni = Column("dni", String(8), unique=True, index=True, nullable=False)
    first_name = Column("nombres", String(100), nullable=False)
    last_name = Column("apellidos", String(100), nullable=False)
    email = Column("email", String(150), nullable=True)
    phone = Column("telefono", String(20), nullable=True)
    address = Column("direccion", Text, nullable=True)
    created_at = Column("creado_en", DateTime(timezone=True), server_default=func.now())

    # Relación uno a muchos con los trámites del ciudadano
    procedures = relationship("Procedure", back_populates="citizen")

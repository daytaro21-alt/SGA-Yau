from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class Procedure(Base):
    """
    Representa un trámite documental ingresado a la municipalidad.
    Mapea a la tabla 'tramites' de la base de datos.
    Contiene campos específicos para el análisis de Machine Learning/NLP.
    """
    __tablename__ = "tramites"

    id = Column("id", Integer, primary_key=True, index=True)
    unique_code = Column("codigo_unico", String(50), unique=True, index=True, nullable=False)
    citizen_id = Column("ciudadano_id", Integer, ForeignKey("ciudadanos.id", ondelete="RESTRICT"), nullable=False)
    title = Column("titulo", String(255), nullable=False)
    description = Column("descripcion", Text, nullable=False)
    extracted_text = Column("texto_extraido", Text, nullable=True)
    procedure_type = Column("tipo_tramite", String(100), nullable=False)
    status_id = Column("estado_id", Integer, ForeignKey("estados_tramite.id", ondelete="RESTRICT"), nullable=False)
    
    # Atributos específicos de Machine Learning / IA
    suggested_priority = Column("prioridad_sugerida", String(20), nullable=True)
    real_priority = Column("prioridad_real", String(20), nullable=True)
    prediction_confidence = Column("confianza_prediccion", Numeric(5, 4), nullable=True)
    model_version = Column("modelo_version", String(50), nullable=True)
    prediction_metadata = Column("prediccion_metadatos", JSONB, nullable=True)
    
    created_at = Column("fecha_creacion", DateTime(timezone=True), server_default=func.now())
    updated_at = Column("fecha_actualizacion", DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones ORM
    citizen = relationship("Citizen", back_populates="procedures")
    status = relationship("ProcedureStatus")

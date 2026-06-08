from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class ProcedureBase(BaseModel):
    """
    Esquema base para un Trámite Documental.
    """
    title: str = Field(..., description="Título o asunto principal del trámite")
    description: str = Field(..., description="Descripción detallada de la solicitud del ciudadano")
    procedure_type: str = Field(..., description="Tipo o categoría del trámite (ej. Mesa de Partes, Obras)")
    extracted_text: Optional[str] = Field(None, description="Texto adicional extraído mediante OCR")

class ProcedureCreate(ProcedureBase):
    """
    Esquema para la creación de un nuevo Trámite.
    """
    citizen_id: int = Field(..., description="ID del ciudadano asociado al trámite")

class ProcedureResponse(ProcedureBase):
    """
    Esquema para responder con la información del Trámite.
    """
    id: int
    unique_code: str
    status_id: int
    suggested_priority: Optional[str] = None
    real_priority: Optional[str] = None
    prediction_confidence: Optional[float] = None
    model_version: Optional[str] = None
    prediction_metadata: Optional[Any] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

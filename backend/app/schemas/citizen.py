from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CitizenBase(BaseModel):
    """
    Esquema base para un Ciudadano.
    """
    dni: str = Field(..., min_length=8, max_length=8, description="DNI del ciudadano (8 dígitos)")
    first_name: str = Field(..., description="Nombres del ciudadano")
    last_name: str = Field(..., description="Apellidos del ciudadano")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico de contacto")
    phone: Optional[str] = Field(None, description="Teléfono de contacto")
    address: Optional[str] = Field(None, description="Dirección del ciudadano")

class CitizenCreate(CitizenBase):
    """
    Esquema para la creación de un nuevo Ciudadano.
    """
    pass

class CitizenResponse(CitizenBase):
    """
    Esquema para devolver los datos de un Ciudadano.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

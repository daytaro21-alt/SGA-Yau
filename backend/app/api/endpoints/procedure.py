from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.procedure import ProcedureCreate, ProcedureResponse
from app.services.procedure_service import ProcedureService

router = APIRouter()

@router.post("/", response_model=ProcedureResponse, status_code=status.HTTP_201_CREATED)
def create_procedure(procedure_data: ProcedureCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva solicitud o trámite documental para un ciudadano.
    """
    return ProcedureService.create_procedure(db, procedure_data)

@router.get("/{id_ciudadano}", response_model=list[ProcedureResponse])
def get_procedures_by_citizen(id_ciudadano: int, db: Session = Depends(get_db)):
    """
    Consulta todos los trámites registrados pertenecientes a un ciudadano específico.
    """
    return ProcedureService.get_procedures_by_citizen(db, id_ciudadano)

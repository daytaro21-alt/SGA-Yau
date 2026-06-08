from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.citizen import CitizenCreate, CitizenResponse
from app.services.citizen_service import CitizenService

router = APIRouter()

@router.post("/", response_model=CitizenResponse, status_code=status.HTTP_201_CREATED)
def create_citizen(citizen_data: CitizenCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo ciudadano en el sistema de SGA-Yau.
    """
    return CitizenService.create_citizen(db, citizen_data)

@router.get("/", response_model=list[CitizenResponse])
def get_citizens(db: Session = Depends(get_db)):
    """
    Lista todos los ciudadanos registrados en el sistema.
    """
    return CitizenService.get_all_citizens(db)

@router.get("/{citizen_id}", response_model=CitizenResponse)
def get_citizen(citizen_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de un ciudadano por su ID único.
    """
    return CitizenService.get_citizen_by_id(db, citizen_id)

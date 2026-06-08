from sqlalchemy.orm import Session
from app.models.citizen import Citizen
from app.schemas.citizen import CitizenCreate
from fastapi import HTTPException, status

class CitizenService:
    """
    Servicio encargado de la lógica de negocio para la gestión de ciudadanos.
    """
    
    @staticmethod
    def create_citizen(db: Session, citizen_data: CitizenCreate) -> Citizen:
        """
        Registra un nuevo ciudadano en el sistema tras validar que su DNI no esté duplicado.
        """
        existing_citizen = db.query(Citizen).filter(Citizen.dni == citizen_data.dni).first()
        if existing_citizen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un ciudadano registrado con el DNI {citizen_data.dni}."
            )
            
        new_citizen = Citizen(
            dni=citizen_data.dni,
            first_name=citizen_data.first_name,
            last_name=citizen_data.last_name,
            email=citizen_data.email,
            phone=citizen_data.phone,
            address=citizen_data.address
        )
        
        db.add(new_citizen)
        db.commit()
        db.refresh(new_citizen)
        return new_citizen

    @staticmethod
    def get_citizen_by_id(db: Session, citizen_id: int) -> Citizen:
        """
        Busca y retorna un ciudadano por su identificador único.
        """
        citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()
        if not citizen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ciudadano con ID {citizen_id} no encontrado."
            )
        return citizen

    @staticmethod
    def get_all_citizens(db: Session) -> list[Citizen]:
        """
        Retorna la lista de todos los ciudadanos registrados.
        """
        return db.query(Citizen).all()

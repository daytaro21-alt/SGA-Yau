import uuid
from sqlalchemy.orm import Session
from app.models.procedure import Procedure
from app.models.citizen import Citizen
from app.models.status import ProcedureStatus
from app.schemas.procedure import ProcedureCreate
from fastapi import HTTPException, status

class ProcedureService:
    """
    Servicio encargado de la lógica de negocio para la gestión de trámites documentales.
    """
    
    @staticmethod
    def create_procedure(db: Session, procedure_data: ProcedureCreate) -> Procedure:
        """
        Crea y registra un nuevo trámite en el sistema asociado a un ciudadano.
        Genera automáticamente un código de trámite único y asigna el estado 'Pendiente'.
        """
        # 1. Validar que el ciudadano exista
        citizen = db.query(Citizen).filter(Citizen.id == procedure_data.citizen_id).first()
        if not citizen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ciudadano con ID {procedure_data.citizen_id} no encontrado."
            )
            
        # 2. Buscar el estado inicial 'Pendiente' en la base de datos
        initial_status = db.query(ProcedureStatus).filter(ProcedureStatus.name == "Pendiente").first()
        if not initial_status:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="El estado inicial 'Pendiente' no se encuentra configurado en el sistema."
            )

        # 3. Generar un código único único para el seguimiento
        unique_code = f"YAU-{uuid.uuid4().hex[:8].upper()}"

        # 4. Crear la entidad de base de datos
        new_procedure = Procedure(
            unique_code=unique_code,
            citizen_id=procedure_data.citizen_id,
            title=procedure_data.title,
            description=procedure_data.description,
            extracted_text=procedure_data.extracted_text,
            procedure_type=procedure_data.procedure_type,
            status_id=initial_status.id,
            # Los campos del modelo de Machine Learning inician vacíos hasta la clasificación asíncrona
            suggested_priority=None,
            real_priority=None,
            prediction_confidence=None,
            model_version=None,
            prediction_metadata=None
        )

        db.add(new_procedure)
        db.commit()
        db.refresh(new_procedure)

        # NOTA DE INTEGRACIÓN ML:
        # En esta fase se podría despachar una tarea asíncrona (ej. Celery, BackgroundTasks de FastAPI)
        # para invocar al modelo NLP que analizará el texto en `new_procedure.description` y/o 
        # `new_procedure.extracted_text` para predecir la prioridad sugerida.

        return new_procedure

    @staticmethod
    def get_procedures_by_citizen(db: Session, citizen_id: int) -> list[Procedure]:
        """
        Retorna la lista de trámites asociados a un ciudadano específico.
        """
        # Validar existencia del ciudadano antes de retornar
        citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()
        if not citizen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ciudadano con ID {citizen_id} no encontrado."
            )

        return db.query(Procedure).filter(Procedure.citizen_id == citizen_id).all()

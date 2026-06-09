from fastapi import APIRouter
from app.api.endpoints.procedure import router as procedure_router
from app.api.endpoints.citizen import router as citizen_router
from app.api.endpoints.cv import router as cv_router

api_router = APIRouter()

# Registrar los enrutadores de los componentes
api_router.include_router(procedure_router, prefix="/tramites", tags=["Trámites"])
api_router.include_router(citizen_router, prefix="/ciudadanos", tags=["Ciudadanos"])
api_router.include_router(cv_router, prefix="/cv", tags=["Evaluación de CV"])

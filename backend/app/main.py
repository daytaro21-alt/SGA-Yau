from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.services.predictor import load_model

# Inicializar la aplicación FastAPI con configuraciones de documentación
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API del Sistema de Gestión Automatizada para la Municipalidad Provincial de Yau (SGA-Yau).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cargar el modelo de NLP globalmente en memoria durante el inicio del servidor
@app.on_event("startup")
def startup_event():
    load_model()

# Configurar CORS (Cross-Origin Resource Sharing)
# Permite solicitudes desde la aplicación móvil Android y clientes web durante el desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incorporar las rutas agrupadas del sistema
app.include_router(api_router)

@app.get("/", tags=["General"])
def read_root():
    """
    Endpoint de bienvenida y estado del servicio.
    """
    return {
        "name": settings.PROJECT_NAME,
        "status": "online",
        "documentation_url": "/docs"
    }

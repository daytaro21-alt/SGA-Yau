from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.services.cv_service import CVService

router = APIRouter()

@router.post("/evaluar/", status_code=status.HTTP_200_OK)
async def evaluar_cv(
    cv_file: UploadFile = File(..., description="Archivo PDF del Currículum Vitae (CV) del candidato"),
    job_description: str = Form(..., description="Requisitos y descripción del puesto de trabajo municipal")
):
    """
    Evalúa la compatibilidad de un CV cargado en formato PDF frente a la descripción de un puesto.
    Retorna el porcentaje de compatibilidad y las habilidades técnicas extraídas.
    """
    # Validar la extensión del archivo cargado
    if not cv_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo cargado debe ser exclusivamente en formato PDF."
        )

    try:
        # Leer el contenido en bytes del archivo cargado
        contenido_pdf = await cv_file.read()
        
        # Extraer el texto plano usando la capa de servicio
        texto_cv = CVService.extraer_texto_pdf(contenido_pdf)
        
        if not texto_cv.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo PDF no contiene texto plano procesable (podría requerir procesamiento OCR)."
            )

        # Calcular la similitud del coseno usando TF-IDF
        porcentaje_compatibilidad = CVService.calcular_similitud(job_description, texto_cv)
        
        # Analizar habilidades técnicas del texto del CV
        habilidades = CVService.extraer_habilidades(texto_cv)
        
        return {
            "filename": cv_file.filename,
            "compatibility_score": porcentaje_compatibilidad,
            "extracted_skills": habilidades
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo interno en el procesamiento del CV: {str(e)}"
        )

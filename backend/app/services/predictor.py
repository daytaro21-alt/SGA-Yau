import os
import joblib
import logging

# Configurar logger
logger = logging.getLogger(__name__)

# Ruta absoluta donde el volumen monta el modelo dentro del contenedor Docker
MODEL_PATH = "/app/models/modelo_prioridad.pkl"

# Variable global que contendrá el pipeline (Vectorizador + Clasificador) en memoria
_model = None

def load_model():
    """
    Carga el modelo de prioridad desde el disco de forma global si no está en memoria.
    Posee un fallback local para facilitar pruebas de desarrollo fuera del contenedor.
    """
    global _model
    if _model is None:
        if os.path.exists(MODEL_PATH):
            try:
                _model = joblib.load(MODEL_PATH)
                logger.info(f"Modelo cargado de manera global desde: {MODEL_PATH}")
            except Exception as e:
                logger.error(f"Error al deserializar el modelo en {MODEL_PATH}: {e}")
                raise e
        else:
            # Fallback para pruebas fuera del contenedor Docker
            fallback_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml_engine", "models", "modelo_prioridad.pkl")
            )
            if os.path.exists(fallback_path):
                try:
                    _model = joblib.load(fallback_path)
                    logger.info(f"Modelo cargado desde la ruta fallback local: {fallback_path}")
                except Exception as e:
                    logger.error(f"Error al deserializar el modelo fallback en {fallback_path}: {e}")
                    raise e
            else:
                logger.warning(
                    f"El archivo del modelo de Machine Learning no fue encontrado en {MODEL_PATH} ni en {fallback_path}."
                )

def predecir(texto: str) -> tuple[str, float]:
    """
    Realiza la inferencia del modelo NLP para un texto determinado.
    Retorna una tupla: (prioridad_sugerida, confianza_prediccion).
    """
    global _model
    # Asegurar que el modelo esté cargado en memoria
    if _model is None:
        load_model()

    if _model is None:
        # Fallback de seguridad en caso de que no exista modelo entrenado aún
        logger.error("Modelo no cargado. Usando fallback de prioridad por defecto (Media).")
        return "Media", 0.5000

    try:
        # Generar la predicción de clase directa
        clase_predicha = _model.predict([texto])[0]
        
        # Obtener las probabilidades de cada clase para calcular la confianza
        probabilidades = _model.predict_proba([texto])[0]
        clases = list(_model.classes_)
        indice_clase = clases.index(clase_predicha)
        
        # Confianza es la probabilidad de la clase seleccionada (0.0000 a 1.0000)
        confianza = float(probabilidades[indice_clase])
        
        return str(clase_predicha), confianza
    except Exception as e:
        logger.error(f"Error durante el proceso de inferencia: {e}")
        # Retorno seguro en caso de fallos inesperados
        return "Media", 0.0000

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

def entrenar_pipeline_prioridad():
    """
    Pipeline de NLP para clasificar la prioridad de trámites municipales.
    Incluye las fases de Carga, Ingesta, Entrenamiento, Evaluación y Persistencia.
    """
    # 1. INGESTA Y PREPROCESAMIENTO DE DATOS
    ruta_dataset = os.path.join("ml_engine", "data", "tramites_historicos.csv")
    if not os.path.exists(ruta_dataset):
        raise FileNotFoundError(f"No se encontró el dataset en la ruta especificada: {ruta_dataset}")
    
    # Cargar el archivo CSV
    datos = pd.read_csv(ruta_dataset)
    print(f"Dataset cargado con éxito. Total registros: {len(datos)}")

    # Combinar 'asunto' y 'descripcion' para enriquecer las características del texto
    datos["texto_completo"] = datos["asunto"] + " " + datos["descripcion"]

    # Separar variables independientes (X) y dependiente (y)
    X = datos["texto_completo"]
    y = datos["prioridad_real"]

    # 2. DIVISIÓN DEL DATASET (80% Entrenamiento, 20% Prueba)
    # Fija semilla aleatoria en 42 para reproducibilidad (Directiva de ml_engine.md)
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Datos divididos: {len(X_entrenamiento)} para entrenamiento, {len(X_prueba)} para prueba.")

    # 3. DEFINICIÓN DEL PIPELINE DE SCICIT-LEARN
    # Lista básica de palabras de parada (stop words) en español para optimizar la tokenización
    palabras_parada_es = [
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 
        'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'mas', 'pero', 
        'sus', 'le', 'ya', 'o', 'este', 'si', 'porque', 'esta', 'entre', 'cuando', 
        'muy', 'sin', 'sobre', 'tambien', 'me', 'hasta', 'desde', 'nos', 'durante', 
        'uno', 'ni', 'contra', 'les'
    ]

    # Pipeline que encadena el Vectorizador TF-IDF y el Clasificador Random Forest
    pipeline = Pipeline([
        ('vectorizador', TfidfVectorizer(
            stop_words=palabras_parada_es,
            ngram_range=(1, 2),  # Considera unigramas y bigramas para capturar frases clave
            max_features=5000
        )),
        ('clasificador', RandomForestClassifier(
            n_estimators=150,
            random_state=42,    # Garantiza que el entrenamiento sea reproducible
            n_jobs=-1           # Utiliza todos los procesadores disponibles
        ))
    ])

    # 4. ENTRENAMIENTO DEL MODELO
    print("Iniciando el entrenamiento del modelo Random Forest...")
    pipeline.fit(X_entrenamiento, y_entrenamiento)
    print("Entrenamiento completado.")

    # 5. EVALUACIÓN DEL PIPELINE
    predicciones = pipeline.predict(X_prueba)
    
    exactitud = accuracy_score(y_prueba, predicciones)
    print(f"\n==============================================")
    print(f"Exactitud Global (Accuracy): {exactitud:.4f}")
    print(f"==============================================")
    print("Reporte de Clasificación Detallado:")
    print(classification_report(y_prueba, predicciones))
    print(f"==============================================")

    # 6. PERSISTENCIA DEL MODELO
    ruta_modelos = os.path.join("ml_engine", "models")
    os.makedirs(ruta_modelos, exist_ok=True)
    
    ruta_guardado = os.path.join(ruta_modelos, "modelo_prioridad.pkl")
    joblib.dump(pipeline, ruta_guardado)
    print(f"Modelo y vectorizador guardados exitosamente en: {ruta_guardado}")

if __name__ == "__main__":
    entrenar_pipeline_prioridad()

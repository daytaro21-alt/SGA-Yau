---
trigger: manual
---

# Directivas de Desarrollo: Machine Learning (Clasificación NLP)

1. **Stack Tecnológico:** Utiliza Python con librerías estándar de la industria (Scikit-Learn, Pandas, NumPy, NLTK o Spacy). Para NLP ligero, prioriza TF-IDF con Random Forest o SVM antes de saltar a modelos Deep Learning.
2. **Modularidad:** El pipeline de ML debe estar dividido en tres fases claras: Ingesta/Limpieza de datos, Entrenamiento y Predicción/Inferencia.
3. **Persistencia:** Guarda los modelos entrenados en la carpeta `models/` utilizando `joblib` o `pickle`.
4. **Reproducibilidad:** Fija siempre una semilla aleatoria (`random_state=42`) para garantizar que los entrenamientos sean reproducibles.
5. **Evaluación:** El código de entrenamiento siempre debe imprimir un reporte de métricas incluyendo Accuracy, Precision, Recall y F1-Score.
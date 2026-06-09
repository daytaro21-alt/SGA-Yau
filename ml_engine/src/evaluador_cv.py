import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extraer_texto_pdf(ruta_pdf: str) -> str:
    """
    Lee un archivo PDF y extrae todo su contenido de texto.
    """
    if not os.path.exists(ruta_pdf):
        raise FileNotFoundError(f"El archivo PDF no fue encontrado en: {ruta_pdf}")
        
    texto_extraido = ""
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for num_pagina, pagina in enumerate(lector.pages):
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_extraido += texto_pagina + "\n"
    return texto_extraido

def calcular_similitud_cv(texto_puesto: str, texto_cv: str) -> float:
    """
    Calcula el porcentaje de compatibilidad entre el perfil del puesto
    y el currículo (CV) usando TF-IDF y Similitud de Coseno.
    """
    # Lista básica de palabras vacías (stop words) en español para filtrar ruido
    palabras_parada_es = [
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 
        'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'mas', 'pero', 
        'sus', 'le', 'ya', 'o', 'este', 'si', 'porque', 'esta', 'entre', 'cuando', 
        'muy', 'sin', 'sobre', 'tambien', 'me', 'hasta', 'desde', 'nos', 'durante', 
        'uno', 'ni', 'contra', 'les'
    ]

    # Inicializar el vectorizador TF-IDF
    vectorizador = TfidfVectorizer(stop_words=palabras_parada_es)

    # Ajustar y transformar los textos en vectores
    vectores = vectorizador.fit_transform([texto_puesto, texto_cv])

    # Calcular la similitud de coseno entre el vector del puesto (0) y el del CV (1)
    similitud = cosine_similarity(vectores[0], vectores[1])[0][0]

    # Convertir a porcentaje de 0 a 100 y redondear a dos decimales
    porcentaje_compatibilidad = round(similitud * 100, 2)
    return porcentaje_compatibilidad

if __name__ == '__main__':
    # Texto simulado del perfil del puesto solicitado por la municipalidad
    perfil_puesto = (
        "Se busca Técnico en Soporte de TI para la Municipalidad Provincial de Yau. "
        "Responsable de brindar soporte técnico de hardware y software a usuarios de la institución. "
        "Requisitos: mantenimiento preventivo y correctivo de computadoras y laptops, configuración "
        "de impresoras en red, soporte en sistemas operativos Windows y Linux, direccionamiento IP, "
        "configuración de redes locales (TCP/IP) y excelente capacidad de atención al usuario."
    )

    # Texto simulado del Currículum Vitae (CV) del postulante
    curriculum_vitae = (
        "Profesional Técnico en Computación e Informática con 3 años de experiencia en soporte técnico "
        "de TI y mesa de ayuda. Especialista en mantenimiento preventivo y correctivo de computadoras de escritorio "
        "y laptops. Amplia experiencia en instalación y configuración de software corporativo y sistemas operativos "
        "Windows. Conocimiento en direccionamiento de red TCP/IP, cableado estructurado y configuración de impresoras. "
        "Habilidades de comunicación orientadas a la atención y soporte al cliente final."
    )

    print("--- Prueba Local de Similitud de CV ---")
    print(f"Perfil del Puesto:\n{perfil_puesto}\n")
    print(f"Currículum Postulante:\n{curriculum_vitae}\n")
    
    porcentaje = calcular_similitud_cv(perfil_puesto, curriculum_vitae)
    print(f"Resultado de compatibilidad matemática: {porcentaje}%")

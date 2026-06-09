import io
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CVService:
    """
    Servicio de procesamiento de currículos (CV) y cálculo de compatibilidad de perfiles.
    """

    @staticmethod
    def extraer_texto_pdf(contenido_binario: bytes) -> str:
        """
        Extrae y unifica el texto plano contenido en el flujo binario de un archivo PDF.
        """
        texto_completo = ""
        flujo_bytes = io.BytesIO(contenido_binario)
        try:
            lector = PyPDF2.PdfReader(flujo_bytes)
            for pagina in lector.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo += texto_pagina + "\n"
        except Exception as e:
            raise ValueError(f"No fue posible leer el archivo PDF: {str(e)}")
        return texto_completo

    @staticmethod
    def calcular_similitud(texto_puesto: str, texto_cv: str) -> float:
        """
        Calcula la compatibilidad porcentual usando la similitud del coseno
        de vectores TF-IDF filtrando palabras vacías en español.
        """
        palabras_parada_es = [
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 
            'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'mas', 'pero', 
            'sus', 'le', 'ya', 'o', 'este', 'si', 'porque', 'esta', 'entre', 'cuando', 
            'muy', 'sin', 'sobre', 'tambien', 'me', 'hasta', 'desde', 'nos', 'durante', 
            'uno', 'ni', 'contra', 'les'
        ]

        vectorizador = TfidfVectorizer(stop_words=palabras_parada_es)
        vectores = vectorizador.fit_transform([texto_puesto, texto_cv])
        
        similitud = cosine_similarity(vectores[0], vectores[1])[0][0]
        return round(float(similitud) * 100, 2)

    @staticmethod
    def extraer_habilidades(texto_cv: str) -> str:
        """
        Analiza el texto del CV para identificar términos de habilidades técnicas relevantes.
        """
        diccionario_habilidades = [
            "soporte", "hardware", "software", "redes", "tcp/ip", "windows", "linux",
            "servidores", "mantenimiento", "impresoras", "ofimática", "excel", "word",
            "atención al cliente", "mesa de ayuda", "programación", "python", "java", "sql",
            "bases de datos", "gestión documental", "archivo", "itse", "seguridad", 
            "obras", "licencias", "atención", "cliente"
        ]
        
        texto_min = texto_cv.lower()
        habilidades_detectadas = []
        for hab in diccionario_habilidades:
            if hab in texto_min:
                habilidades_detectadas.append(hab.capitalize())
                
        if not habilidades_detectadas:
            return "General / No especificadas"
        return ", ".join(habilidades_detectadas)

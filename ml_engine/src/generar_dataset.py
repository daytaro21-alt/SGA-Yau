import os
import random
import pandas as pd
from faker import Faker

def generar_dataset_historico(num_registros=5000):
    """
    Genera un dataset simulado de trámites municipales con correlación lógica
    entre palabras clave en la descripción y la prioridad real (etiqueta objetivo).
    """
    # Configuración de reproducibilidad (Directiva de ml_engine.md)
    random.seed(42)
    Faker.seed(42)
    
    # Inicializar Faker con localización en español
    fake = Faker('es_ES')
    
    # Categorías de trámites reales indicadas por el usuario
    tipos_tramite = [
        'Licencia de Funcionamiento',
        'Licencia de Edificación',
        'Inspección Técnica de Seguridad (ITSE)',
        'Queja por Servicios',
        'Constancia de Posesión'
    ]
    
    # Plantillas de textos segmentadas por nivel de prioridad para generar correlación lógica
    plantillas_urgente_alta = [
        "Se presenta una situación de emergencia por {problema} en {lugar}. Existe un riesgo estructural inminente.",
        "Reporto peligro de colapso en {lugar} debido a {problema}. Solicito inspección de inmediato.",
        "Fuga de agua masiva y riesgo de corto circuito en {lugar}. Requiero intervención urgente por peligro inminente.",
        "Solicitud de inspección extraordinaria de seguridad en {lugar} debido a grietas graves y amenaza de derrumbe.",
        "Denuncia de riesgo estructural crítico en {lugar} por {problema}. Se teme daño físico a las personas.",
        "Se solicita apoyo de inmediato por {problema} que amenaza la seguridad pública en {lugar}."
    ]

    plantillas_media_normal = [
        "Solicito la renovación de mi licencia de funcionamiento para el establecimiento comercial ubicado en {lugar}.",
        "Presento la solicitud de regularización de mi constancia de posesión del predio ubicado en {lugar}.",
        "Requiero una inspección técnica de seguridad (ITSE) de rutina para el local comercial en {lugar}.",
        "Solicitud de licencia de edificación para ampliación de vivienda residencial en {lugar}.",
        "Queja por servicios debido a fallas intermitentes en el alumbrado público de {lugar}.",
        "Trámite regular para obtener la constancia de posesión del terreno denominado {lugar}."
    ]

    plantillas_baja = [
        "Solicitud de copia certificada de la resolución de alcaldía emitida el año pasado sobre el predio {lugar}.",
        "Realizo una consulta simple para solicitar información sobre los requisitos del trámite de {tramite}.",
        "Solicito duplicado del certificado de habitabilidad de la propiedad en {lugar}.",
        "Consulta sobre el estado actual de mi trámite administrativo Nro. {codigo} presentado anteriormente.",
        "Solicito información general sobre los planos catastrales de la zona de {lugar}.",
        "Pedido de copias de actas de la junta vecinal de {lugar} correspondientes al periodo anterior."
    ]

    # Problemas simulados para las solicitudes urgentes
    problemas = [
        "filtraciones severas de agua en las columnas",
        "grietas profundas en los muros de carga",
        "deslizamiento de tierra en el talud colindante",
        "cables eléctricos expuestos a la intemperie",
        "hundimiento del suelo en el patio principal",
        "debilitamiento de vigas por humedad extrema"
    ]

    datos = []

    for idx in range(1, num_registros + 1):
        codigo_unico = f"YAU-HIST-{100000 + idx}"
        tipo = random.choice(tipos_tramite)
        
        # Determinar prioridad y seleccionar plantilla adecuada (creando correlación)
        rand_val = random.random()
        
        if rand_val < 0.15:
            # Urgente
            prioridad = "Urgente"
            plantilla = random.choice(plantillas_urgente_alta)
            problema = random.choice(problemas)
            direccion = fake.street_address()
            descripcion = plantilla.format(problema=problema, lugar=direccion)
            asunto = f"EMERGENCIA: {tipo} por {problema}"
            
        elif rand_val < 0.35:
            # Alta
            prioridad = "Alta"
            plantilla = random.choice(plantillas_urgente_alta)
            problema = random.choice(problemas)
            direccion = fake.street_address()
            descripcion = plantilla.format(problema=problema, lugar=direccion)
            asunto = f"Urgente: Solicitud de {tipo} por riesgo"
            
        elif rand_val < 0.75:
            # Media
            prioridad = "Media"
            plantilla = random.choice(plantillas_media_normal)
            direccion = fake.street_address()
            descripcion = plantilla.format(lugar=direccion)
            asunto = f"Trámite de {tipo} - {fake.word().capitalize()}"
            
        else:
            # Baja
            prioridad = "Baja"
            plantilla = random.choice(plantillas_baja)
            direccion = fake.street_address()
            descripcion = plantilla.format(
                lugar=direccion, 
                tramite=tipo.lower(), 
                codigo=f"EXP-{random.randint(1000, 9999)}"
            )
            asunto = f"Consulta / Copia: {tipo}"

        datos.append({
            "codigo_unico": codigo_unico,
            "asunto": asunto,
            "descripcion": descripcion,
            "tipo_tramite": tipo,
            "prioridad_real": prioridad
        })

    df = pd.DataFrame(datos)
    
    # Asegurar que la ruta exista antes de guardar
    ruta_salida = os.path.join("ml_engine", "data", "tramites_historicos.csv")
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Guardar a CSV
    df.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(f"Dataset generado exitosamente con {len(df)} registros.")
    print(f"Archivo guardado en: {ruta_salida}")
    print("\nDistribución de prioridades:")
    print(df["prioridad_real"].value_counts())

if __name__ == "__main__":
    generar_dataset_historico(5000)

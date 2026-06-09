import random
import time
import requests

# URL del servidor local de FastAPI
BASE_URL = "http://localhost:8000"

# Listas de datos para generación realista (referencias a Piura, Perú)
nombres = [
    "Juan", "Pedro", "Maria", "Rosa", "Luis", "Carlos", "Jose", "Ana", 
    "Jorge", "Miguel", "Carmen", "Sofia", "Diego", "Elena", "Gabriel", 
    "Lucia", "Manuel", "Patricia", "Fernando", "Teresa"
]

apellidos = [
    "Garcia", "Rodriguez", "Flores", "Cruz", "Ramirez", "Zapata", "Sandoval", 
    "Lopez", "Castro", "Ruiz", "Chunga", "Seminario", "Vilchez", "More", 
    "Yarleque", "Neyra", "Cordova", "Guerrero", "Peña", "Benites"
]

direcciones = [
    "Urb. Miraflores Mz. A Lt. 15, Castilla",
    "Av. Sánchez Cerro 1245, Piura",
    "Calle Tacna 452, Catacaos",
    "Jr. Huancavelica 782, Piura",
    "Asoc. Santa Rosa Mz. F, Veintiséis de Octubre",
    "Calle Libertad 120, Catacaos",
    "Jr. Arequipa 550, Castilla",
    "Av. Grau 890, Piura",
    "Calle Comercio 312, Catacaos",
    "A.H. San Martin Calle 4, Veintiséis de Octubre"
]

tipos_tramite = [
    'Licencia de Funcionamiento',
    'Licencia de Edificación',
    'Inspección Técnica de Seguridad (ITSE)',
    'Queja por Servicios',
    'Constancia de Posesión'
]

# Banco estratégico de 15 plantillas categorizadas por prioridad (Urgente/Alta vs Media/Baja)
# Diseñado específicamente para activar las lógicas entrenadas en el modelo NLP
banco_tramites = [
    # --- GRUPO 1: Prioridad Urgente / Alta ---
    {
        "titulo": "Emergencia por peligro de colapso de infraestructura",
        "tipo": "Inspección Técnica de Seguridad (ITSE)",
        "descripcion": "Reporto de forma urgente un peligro de colapso inminente en la pared lateral de mi vivienda debido al debilitamiento de las vigas. Solicito inspección inmediata."
    },
    {
        "titulo": "Riesgo estructural crítico en local comercial",
        "tipo": "Inspección Técnica de Seguridad (ITSE)",
        "descripcion": "Denuncia de riesgo estructural severo en el establecimiento comercial vecino. Presenta grietas profundas y peligro de derrumbe de un muro sobre la vereda."
    },
    {
        "titulo": "Urgente: Caída de poste de alumbrado en vía pública",
        "tipo": "Queja por Servicios",
        "descripcion": "Reporto la caída de poste de luz en la calle principal. Hay cables expuestos de alta tensión a la intemperie, lo cual representa un peligro inminente para los vecinos."
    },
    {
        "titulo": "Solicitud de apoyo inmediato ante deslizamiento de tierra",
        "tipo": "Constancia de Posesión",
        "descripcion": "Se solicita apoyo de emergencia de defensa civil debido a un deslizamiento de tierra en el talud colindante a mi predio rústico. Riesgo inminente de sepultamiento."
    },
    {
        "titulo": "Emergencia sanitaria por rotura de desagüe e inundación",
        "tipo": "Queja por Servicios",
        "descripcion": "Urgente: Reporto inundación de aguas servidas en la cuadra por rotura de tubería matriz. El agua está ingresando a mi predio y hay riesgo de contaminación grave."
    },
    {
        "titulo": "Inspección urgente por cortocircuito expuesto",
        "tipo": "Inspección Técnica de Seguridad (ITSE)",
        "descripcion": "Solicitud urgente de inspección extraordinaria en la galería comercial local. Existen cables expuestos con chispas constantes y riesgo de incendio inminente."
    },
    {
        "titulo": "Peligro por muro a punto de ceder en la vía peatonal",
        "tipo": "Inspección Técnica de Seguridad (ITSE)",
        "descripcion": "Reporto un muro antiguo perimetral a punto de ceder sobre el pasadizo común peatonal. Se requiere demolición o apuntalamiento de inmediato."
    },
    
    # --- GRUPO 2: Prioridad Media / Baja ---
    {
        "titulo": "Solicitud de renovación de licencia de bodeguita",
        "tipo": "Licencia de Funcionamiento",
        "descripcion": "Solicito la renovación regular de la licencia de funcionamiento para mi local comercial tipo bodega de abarrotes de nombre comercial 'Abarrotes Piura'."
    },
    {
        "titulo": "Información sobre arbitrios y estado de cuenta predial",
        "tipo": "Queja por Servicios",
        "descripcion": "Requiero información y el estado de cuenta de mis arbitrios municipales correspondientes al presente periodo fiscal para ponerme al día con los pagos."
    },
    {
        "titulo": "Solicitud de copia certificada de partida de nacimiento",
        "tipo": "Constancia de Posesión",
        "descripcion": "Solicito copia de partida de nacimiento certificada de mi menor hijo para fines de matrícula escolar y actualización del documento nacional de identidad."
    },
    {
        "titulo": "Consulta de horarios de atención en mesa de partes",
        "tipo": "Queja por Servicios",
        "descripcion": "Realizo una consulta simple sobre el horario de atención al público de la ventanilla única de mesa de partes durante los días feriados de la próxima semana."
    },
    {
        "titulo": "Solicitud de pago de predial fraccionado",
        "tipo": "Licencia de Edificación",
        "descripcion": "Solicito información para acogerme al beneficio de pago de impuesto predial fraccionado de mi domicilio fiscal ubicado en Castilla."
    },
    {
        "titulo": "Consulta de requisitos para obtener licencia de edificación",
        "tipo": "Licencia de Edificación",
        "descripcion": "Solicito la lista de requisitos y los formatos oficiales necesarios para iniciar un trámite regular de licencia de edificación para una vivienda unifamiliar."
    },
    {
        "titulo": "Solicitud de duplicado de certificado catastral",
        "tipo": "Constancia de Posesión",
        "descripcion": "Solicito un duplicado de la constancia catastral de mi predio rústico emitida en el periodo anterior por extravío del documento físico original."
    },
    {
        "titulo": "Requerimiento de copia de plano de zonificación urbana",
        "tipo": "Licencia de Edificación",
        "descripcion": "Solicito acceso a la información pública para obtener una copia simple en PDF de los planos de zonificación urbana vigentes del distrito."
    }
]

def poblar_sistema():
    print("==========================================================")
    print("🚀 Iniciando Script de Poblado Masivo para SGA-Yau")
    print("==========================================================")
    
    ciudadanos_ids = []

    # 1. Generación de 25 Ciudadanos
    print("\n👥 Registrando 25 Ciudadanos...")
    for i in range(1, 26):
        dni = f"{random.randint(10000000, 99999999)}"
        nombre = random.choice(nombres)
        apellido = f"{random.choice(apellidos)} {random.choice(apellidos)}"
        correo = f"{nombre.lower()}.{apellido.split()[0].lower()}@example.com"
        telefono = f"9{random.randint(10000000, 99999999)}"
        direccion = random.choice(direcciones)

        payload_ciudadano = {
            "dni": dni,
            "first_name": nombre,
            "last_name": apellido,
            "email": correo,
            "phone": telefono,
            "address": direccion
        }

        try:
            res = requests.post(f"{BASE_URL}/ciudadanos/", json=payload_ciudadano)
            if res.status_code == 201:
                datos_res = res.json()
                ciudadanos_ids.append(datos_res["id"])
                print(f"  [Ciudadano {i}/25] Registrado: {nombre} {apellido} (ID: {datos_res['id']})")
            else:
                print(f"  [Error] No se pudo registrar ciudadano {nombre}: {res.text}")
        except Exception as e:
            print(f"  [Fallo de Conexión] No se pudo comunicar con el servidor: {e}")
            return

    if not ciudadanos_ids:
        print("\n❌ Error: No se pudo registrar ningún ciudadano. Abortando creación de trámites.")
        return

    # 2. Generación de 100 Trámites
    print("\n📄 Registrando 100 Trámites con clasificación de Machine Learning...")
    for j in range(1, 101):
        ciudadano_id = random.choice(ciudadanos_ids)
        plantilla = random.choice(banco_tramites)
        
        payload_tramite = {
            "title": plantilla["titulo"],
            "description": plantilla["descripcion"],
            "procedure_type": plantilla["tipo"],
            "citizen_id": ciudadano_id,
            "extracted_text": None
        }

        try:
            res = requests.post(f"{BASE_URL}/tramites/", json=payload_tramite)
            if res.status_code == 201:
                datos_tramite = res.json()
                print(f"  [Trámite {j}/100] Registrado: {datos_tramite['unique_code']} | Prioridad ML: {datos_tramite['suggested_priority']}")
            else:
                print(f"  [Error] No se pudo registrar trámite {j}: {res.text}")
        except Exception as e:
            print(f"  [Fallo de Conexión] Error al enviar trámite {j}: {e}")
            break

        # Pequeño retardo entre peticiones para no saturar el servidor (0.1 segundos)
        time.sleep(0.1)

    print("\n==========================================================")
    print("✅ Proceso Finalizado con éxito.")
    print("==========================================================")

if __name__ == "__main__":
    poblar_sistema()

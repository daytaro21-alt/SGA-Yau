import streamlit as st
import requests
import os

# Configuración de página de Streamlit
st.set_page_config(
    page_title="SGA-Yau - Administración",
    page_icon="🏛️",
    layout="wide"
)

# Estilos personalizados para mejorar la estética visual
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Fondo general tipo Dashboard */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
    }

    /* Estructura de la Tarjeta */
    .custom-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 1px solid #f3f4f6;
        padding-bottom: 16px;
        margin-bottom: 16px;
    }

    .priority-badge {
        font-size: 13px;
        font-weight: 600;
        padding: 6px 16px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Caja de la descripción */
    .desc-box {
        background-color: #f9fafb;
        padding: 16px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        color: #374151;
        font-size: 15px;
        line-height: 1.5;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Sistema de Gestión Automatizada - SGA-Yau</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Panel Administrativo de la Municipalidad Provincial de Yau</div>', unsafe_allow_html=True)
st.markdown("---")

# Menú lateral para la navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.radio(
    "Seleccione un módulo:",
    ["Gestión de Trámites", "Selección de Personal (RRHH)"]
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

if seccion == "Gestión de Trámites":
    st.header("Control de Trámites Documentales")
    st.markdown("Módulo para consultar los trámites de ciudadanos y la clasificación de prioridades mediante IA.")

    try:
        # 1. Obtener lista de ciudadanos
        respuesta_ciudadanos = requests.get(f"{BACKEND_URL}/ciudadanos/")
        if respuesta_ciudadanos.status_code == 200:
            ciudadanos = respuesta_ciudadanos.json()
            if not ciudadanos:
                st.warning("No hay ciudadanos registrados en el sistema municipal.")
            else:
                # Estructurar opciones del selector
                opciones = {
                    f"{c['first_name']} {c['last_name']} (DNI: {c['dni']})": c['id']
                    for c in ciudadanos
                }
                seleccion_ciudadano = st.selectbox(
                    "Seleccione un ciudadano para ver su historial de trámites:",
                    list(opciones.keys())
                )

                id_ciudadano = opciones[seleccion_ciudadano]

                # 2. Obtener trámites del ciudadano seleccionado
                respuesta_tramites = requests.get(f"{BACKEND_URL}/tramites/{id_ciudadano}")
                if respuesta_tramites.status_code == 200:
                    tramites = respuesta_tramites.json()
                    if not tramites:
                        st.info("Este ciudadano no tiene trámites documentales registrados.")
                    else:
                        st.markdown(f"#### Trámites Encontrados: **{len(tramites)}**")
                        for t in tramites:
                            prioridad = t['suggested_priority']
                            confianza = t['prediction_confidence']
                            
                            # Determinar color según prioridad
                            color_prioridad = "#4f8a8b"
                            if prioridad == "Urgente":
                                color_prioridad = "#ef4444" # Rojo vivo
                            elif prioridad == "Alta":
                                color_prioridad = "#f59e0b" # Naranja
                            elif prioridad == "Media":
                                color_prioridad = "#10b981" # Verde
                            elif prioridad == "Baja":
                                color_prioridad = "#3b82f6" # Azul

                            # Dibujar la tarjeta HTML
                            html_card = f"""
                            <div class="custom-card">
                                <div class="card-header">
                                    <div>
                                        <div style="font-size: 20px; font-weight: 700; color: #111827; display: flex; align-items: center; gap: 8px;">
                                            📄 {t['title']}
                                        </div>
                                        <div style="font-size: 13px; color: #6b7280; margin-top: 6px; font-weight: 500;">
                                            <span style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px; border: 1px solid #e5e7eb;">{t['unique_code']}</span> • {t['procedure_type']}
                                        </div>
                                    </div>
                                    <div style="text-align: right; min-width: 120px;">
                                        <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">Prioridad IA</div>
                                        <span class="priority-badge" style="color: white; background-color: {color_prioridad};">{prioridad if prioridad else "Sin Clasificar"}</span>
                                        <div style="font-size: 12px; color: #9ca3af; margin-top: 8px; font-weight: 500;">Confianza: {float(confianza) * 100:.1f}%</div>
                                    </div>
                                </div>
                                <div style="font-size: 12px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">Descripción del Ciudadano</div>
                                <div class="desc-box">{t['description']}</div>
                            </div>
                            """
                            st.markdown(html_card, unsafe_allow_html=True)
                else:
                    st.error("Error al consultar los trámites del ciudadano seleccionado.")
        else:
            st.error("Error al obtener la lista de ciudadanos.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 No se pudo establecer conexión con el backend de FastAPI. Asegúrese de que el contenedor de la API esté activo.")

elif seccion == "Selección de Personal (RRHH)":
    st.header("Selección de Personal (Recursos Humanos)")
    st.markdown("Evalúe los perfiles de los postulantes contrastando su currículum con la descripción de puestos de la municipalidad.")

    # Formulario de carga
    with st.form("evaluacion_cv_form"):
        perfil_ejemplo = (
            "Se busca Técnico en Soporte de TI para la Municipalidad Provincial de Yau. "
            "Requisitos: soporte de hardware y software, mantenimiento preventivo y correctivo de computadoras "
            "y laptops, configuración de impresoras en red, soporte de redes locales TCP/IP y Windows/Linux."
        )
        job_description = st.text_area(
            "Descripción del Puesto / Requisitos:",
            value=perfil_ejemplo,
            height=150
        )
        
        cv_file = st.file_uploader(
            "Subir Currículum del Candidato (Formato PDF):",
            type=["pdf"]
        )
        
        evaluar_btn = st.form_submit_button("🔍 Evaluar Candidato")

    if evaluar_btn:
        if not cv_file:
            st.warning("Por favor, cargue un currículum en formato PDF para realizar la evaluación.")
        else:
            with st.spinner("Analizando currículum y evaluando similitud..."):
                try:
                    # Enviar el archivo y la descripción mediante una solicitud multipart POST
                    archivos = {
                        "cv_file": (cv_file.name, cv_file.getvalue(), "application/pdf")
                    }
                    datos = {
                        "job_description": job_description
                    }
                    
                    respuesta = requests.post(
                        f"{BACKEND_URL}/cv/evaluar/",
                        files=archivos,
                        data=datos
                    )
                    
                    if respuesta.status_code == 200:
                        resultado = respuesta.json()
                        score = resultado["compatibility_score"]
                        habilidades = resultado["extracted_skills"]
                        
                        st.markdown("### 📊 Reporte de Compatibilidad")
                        
                        c1, c2 = st.columns([1, 2])
                        with c1:
                            color_score = "#5cb85c"
                            if score < 35:
                                color_score = "#d9534f"
                            elif score < 65:
                                color_score = "#f0ad4e"
                                
                            st.markdown("#### Porcentaje de Similitud:")
                            st.markdown(f'<span style="font-size: 56px; font-weight: bold; color: {color_score};">{score}%</span>', unsafe_allow_html=True)
                            st.progress(score / 100.0)
                        
                        with c2:
                            st.markdown("#### Habilidades Técnicas Detectadas:")
                            st.info(habilidades)
                            
                        # Evaluar rango de aptitud
                        if score >= 70:
                            st.success("✨ El postulante califica plenamente para el perfil del puesto solicitado.")
                        elif score >= 40:
                            st.warning("⚠️ El postulante posee compatibilidad parcial con los requerimientos.")
                        else:
                            st.error("❌ El perfil del postulante no se alinea adecuadamente con el puesto.")
                    else:
                        st.error(f"Error en el backend: {respuesta.json().get('detail', 'Error desconocido')}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 No se pudo comunicar con el backend de FastAPI. Verifique que el servicio esté activo.")

-- ============================================================================
-- SQL de Inicialización de Base de Datos - SGA-Yau
-- Sistema de Gestión Automatizada para la Municipalidad Provincial de Yau
-- ============================================================================

-- Tabla para almacenar los estados posibles de un trámite documental
CREATE TABLE IF NOT EXISTS estados_tramite (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para registrar la información de ciudadanos y usuarios administrados
CREATE TABLE IF NOT EXISTS ciudadanos (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(8) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    telefono VARCHAR(20),
    direccion TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de trámites documentales
-- Incluye campos y metadatos específicos para procesamiento NLP y predicción de prioridades
CREATE TABLE IF NOT EXISTS tramites (
    id SERIAL PRIMARY KEY,
    codigo_unico VARCHAR(50) NOT NULL UNIQUE,
    ciudadano_id INT NOT NULL REFERENCES ciudadanos(id) ON DELETE RESTRICT,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,                -- Texto de la solicitud ingresado por el ciudadano
    texto_extraido TEXT,                      -- Texto completo extraído mediante OCR de documentos adjuntos (PDF, imágenes)
    tipo_tramite VARCHAR(100) NOT NULL,        -- Categoría del trámite (ej. Licencia de Funcionamiento, Obras, Quejas)
    estado_id INT NOT NULL REFERENCES estados_tramite(id) ON DELETE RESTRICT,
    
    -- Campos reservados para la integración de Machine Learning (Clasificación NLP)
    prioridad_sugerida VARCHAR(20),           -- Prioridad recomendada por el modelo (ej. Baja, Media, Alta, Urgente)
    prioridad_real VARCHAR(20),               -- Prioridad final corregida o validada por un humano (Ground Truth para entrenamiento)
    confianza_prediccion DECIMAL(5, 4),        -- Grado de certidumbre del modelo (0.0000 a 1.0000)
    modelo_version VARCHAR(50),               -- Identificador de la versión del modelo que predijo
    prediccion_metadatos JSONB,               -- Datos adicionales de inferencia (ej. probabilidades de clases, palabras clave detectadas)
    
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Creación de índices para optimizar consultas de administración y la ingesta de datos en el motor de ML
CREATE INDEX IF NOT EXISTS idx_tramites_estado ON tramites(estado_id);
CREATE INDEX IF NOT EXISTS idx_tramites_codigo ON tramites(codigo_unico);
CREATE INDEX IF NOT EXISTS idx_tramites_prioridad_sugerida ON tramites(prioridad_sugerida);
CREATE INDEX IF NOT EXISTS idx_tramites_prioridad_real ON tramites(prioridad_real);

-- trigger para automatizar el campo fecha_actualizacion
CREATE OR REPLACE FUNCTION actualizar_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_fecha_tramites
    BEFORE UPDATE ON tramites
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_actualizacion();

-- Inserción de estados base para el flujo de gestión documental
INSERT INTO estados_tramite (nombre, descripcion) VALUES
('Pendiente', 'Trámite ingresado al sistema, pendiente de clasificación o asignación inicial.'),
('En Proceso', 'El trámite está siendo evaluado por el área correspondiente.'),
('Observado', 'El trámite tiene observaciones que el ciudadano debe subsanar.'),
('Derivado', 'El trámite ha sido transferido a otra área administrativa.'),
('Aprobado', 'El trámite ha sido resuelto de manera favorable.'),
('Rechazado', 'El trámite ha sido denegado o archivado sin resolución favorable.')
ON CONFLICT (nombre) DO NOTHING;

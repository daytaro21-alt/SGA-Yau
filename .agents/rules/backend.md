---
trigger: manual
---

# Directivas de Desarrollo: Backend (Python & API)

1. **Lenguaje y Framework:** Utiliza Python 3.10+. Si implementas un framework web, prioriza FastAPI por su rendimiento y autogeneración de documentación (Swagger).
2. **Arquitectura:** Aplica separación de responsabilidades. Los controladores (endpoints) no deben contener lógica de negocio; esta debe residir en la capa `services`. 
3. **Base de Datos:** Utiliza PostgreSQL. Emplea un ORM (como SQLAlchemy o SQLModel) para interactuar con la base de datos, evitando consultas SQL crudas a menos que sea estrictamente necesario para rendimiento.
4. **Respuestas:** Todas las respuestas de la API deben devolver formato JSON estructurado y manejar los códigos de estado HTTP correctamente (200, 201, 400, 404, 500).
5. **Idioma:** Código base en inglés (variables, funciones, clases), pero docstrings, comentarios y mensajes de error en español.
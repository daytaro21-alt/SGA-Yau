---
trigger: manual
---

# Directivas de Desarrollo: Infraestructura y Docker

1. **Contenerización:** Todos los servicios (Backend, ML Engine, Base de Datos) deben ejecutarse en contenedores separados.
2. **Imágenes Ligeras:** Utiliza imágenes base oficiales de Alpine o versiones "slim" (ej. `python:3.10-slim`) para mantener los contenedores pequeños y rápidos.
3. **Docker Compose:** Utiliza `docker-compose.yml` para orquestar la comunicación entre servicios. Asegúrate de configurar una red interna para que el backend pueda ver a la base de datos por su nombre de servicio.
4. **Variables de Entorno:** Nunca incluyas contraseñas o credenciales en el código fuente ni en los Dockerfiles. Utiliza un archivo `.env` o pásalas directamente a través del archivo compose.
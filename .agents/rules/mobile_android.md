---
trigger: manual
---

# Directivas de Desarrollo: App Móvil (Android Nativo)

1. **Lenguaje Estricto:** Utiliza exclusivamente Java para el desarrollo de la aplicación Android. No utilices Kotlin.
2. **Estructura de Android Studio:** Respeta la estructura de directorios estándar de Android (`src/main/java` y `src/main/res`).
3. **Persistencia Local:** Si se requiere guardar configuraciones locales o el estado del usuario antes de enviar a la base de datos central, utiliza SQLite o SharedPreferences de manera modularizada.
4. **Llamadas de Red:** Las peticiones al backend deben ser asíncronas para no bloquear el hilo principal (UI thread). Utiliza librerías robustas para peticiones HTTP en Java (como Retrofit o Volley).
5. **Interfaz (UI):** Diseña los layouts en XML utilizando `ConstraintLayout` para asegurar que las pantallas sean responsivas y eficientes en la jerarquía de vistas.
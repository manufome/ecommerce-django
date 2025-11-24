# 🔙 Backend - La Fortaleza API

El backend de **La Fortaleza** es una API RESTful robusta construida con **Django** y **Django Rest Framework (DRF)**. Su objetivo es servir como la fuente central de verdad para la plataforma de comercio electrónico, gestionando la lógica de negocio, la persistencia de datos y la seguridad.

## ⚙️ Características Técnicas

-   **Framework**: Django 5.0 + DRF 3.15
-   **Base de Datos**: PostgreSQL (Producción) / SQLite (Desarrollo rápido)
-   **Autenticación**: JWT (JSON Web Tokens) vía `djangorestframework-simplejwt`
-   **Documentación**: Swagger/OpenAPI generado automáticamente con `drf-yasg`
-   **Manejo de Archivos**: Soporte para carga de imágenes de productos
-   **Estructura**: Arquitectura modular basada en "apps" de Django

Para más detalles sobre la arquitectura, esquemas de base de datos y guías de contribución, consulta la [carpeta de documentación](docs/).

## 🗂️ Estructura de Aplicaciones

El proyecto está modularizado en las siguientes aplicaciones (`/apps`):

-   `users`: Gestión de usuarios, autenticación y perfiles.
-   `shop`: Catálogo de productos, categorías, marcas y gestión de inventario.
-   `orders`: Procesamiento de pedidos, carritos de compra y direcciones.
-   `payments`: Lógica de pagos y transacciones.
-   `shipping`: Cálculo de costos y gestión de envíos.

## 🚀 Instalación y Configuración

### Prerrequisitos
-   Python 3.10 o superior
-   PostgreSQL (opcional para desarrollo, requerido para producción)

### Pasos

1.  **Clonar y entrar al directorio:**
    ```bash
    cd backend
    ```

2.  **Crear entorno virtual:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Variables de Entorno:**
    Crea un archivo `.env` en la raíz de `backend/` basándote en `.env.example`.
    ```ini
    DEBUG=True
    SECRET_KEY=tu_clave_secreta_segura
    ALLOWED_HOSTS=localhost,127.0.0.1
    
    # Base de datos (Ejemplo para PostgreSQL local)
    DB_NAME=la_fortaleza_db
    DB_USER=postgres
    DB_PASSWORD=tu_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5.  **Migraciones y Superusuario:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

6.  **Poblar la Base de Datos (Opcional):**
    Para facilitar el desarrollo y pruebas, puedes poblar la base de datos con datos de ejemplo:
    
    **Opción A - Datos desde CSV:**
    ```bash
    python manage.py populate_shop data/products.csv
    ```
    Este comando lee un archivo CSV con productos reales y crea categorías, marcas, productos e imágenes.
    
    **Opción B - Datos Faker (Aleatorios):**
    ```bash
    python manage.py populate_shop_faker
    ```
    Genera 100 productos aleatorios con 5 categorías y 5 marcas usando la librería Faker.

7.  **Ejecutar Servidor:**
    ```bash
    python manage.py runserver
    ```
    La API estará disponible en `http://localhost:8000`.

## 📖 Documentación de la API

Una vez iniciado el servidor, puedes acceder a la documentación interactiva en:
-   **Swagger UI**: `http://localhost:8000/docs/`
-   **ReDoc**: `http://localhost:8000/redoc/`

## 📦 Despliegue

El proyecto incluye archivos de configuración para despliegue en plataformas como **Heroku** o **Render**:
-   `Procfile`: Define el comando de ejecución con `gunicorn`.
-   `runtime.txt`: Especifica la versión de Python.
-   `whitenoise`: Configurado para servir archivos estáticos en producción.

Para desplegar, asegúrate de configurar las variables de entorno en tu proveedor de hosting.

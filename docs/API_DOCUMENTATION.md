# 📚 Documentación de la API - La Fortaleza

## Descripción

La API de La Fortaleza utiliza **drf-spectacular** para generar documentación OpenAPI 3.0 automática y completa. Esto proporciona una interfaz interactiva para explorar y probar todos los endpoints de la API.

## 🚀 Acceso a la Documentación

Una vez que el servidor esté corriendo, puedes acceder a la documentación en las siguientes URLs:

### Swagger UI (Interactiva)
```
http://localhost:8000/api/docs/
```
- **Interfaz moderna y fácil de usar**
- Permite probar endpoints directamente desde el navegador
- Incluye autenticación JWT integrada
- Muestra ejemplos de request/response

### ReDoc (Lectura)
```
http://localhost:8000/api/redoc/
```
- **Documentación optimizada para lectura**
- Diseño limpio y profesional
- Ideal para compartir con equipos de desarrollo
- Búsqueda integrada

### Schema OpenAPI (JSON)
```
http://localhost:8000/api/schema/
```
- Esquema OpenAPI 3.0 en formato JSON
- Útil para generar clientes automáticos
- Compatible con herramientas como Postman

## 🔐 Autenticación en la Documentación

Para probar endpoints protegidos en Swagger UI:

1. **Obtener Token JWT**:
   - Ve a `/api/v1/auth/login/`
   - Ingresa credenciales válidas
   - Copia el `access` token de la respuesta

2. **Autorizar en Swagger**:
   - Click en el botón **"Authorize"** (candado verde)
   - Ingresa: `Bearer <tu_access_token>`
   - Click en **"Authorize"**
   - Ahora puedes probar endpoints protegidos

## 📋 Endpoints Principales

### Autenticación (`/api/v1/auth/`)
- `POST /login/` - Iniciar sesión
- `POST /register/` - Registrar nuevo usuario
- `POST /token/refresh/` - Refrescar token JWT

### Productos (`/api/v1/shop/`)
- `GET /products/` - Listar productos
- `GET /products/{id}/` - Detalle de producto
- `GET /categories/` - Listar categorías
- `GET /brands/` - Listar marcas

### Pedidos (`/api/v1/orders/`)
- `GET /orders/` - Listar pedidos del usuario
- `POST /orders/` - Crear nuevo pedido
- `GET /addresses/` - Direcciones de envío
- `GET /choices/` - Opciones (localidades, métodos de pago, etc.)

### Admin (`/api/v1/admin/`)
- Endpoints administrativos (requieren permisos de staff)

## 🛠️ Instalación

Las dependencias ya están incluidas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

Paquetes relacionados:
- `djangorestframework==3.15.2`
- `drf-spectacular==0.27.2`

## ⚙️ Configuración

La configuración de drf-spectacular está en `config/settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'La Fortaleza API',
    'DESCRIPTION': 'API RESTful para la plataforma de e-commerce La Fortaleza',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}
```

## 📝 Personalización

### Agregar Descripciones a Endpoints

Puedes mejorar la documentación agregando docstrings a tus vistas:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ProductViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="Listar todos los productos",
        description="Retorna una lista paginada de productos disponibles",
        parameters=[
            OpenApiParameter(
                name='category',
                description='Filtrar por categoría',
                required=False,
                type=int
            ),
        ]
    )
    def list(self, request):
        # ...
```

### Ejemplos de Request/Response

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Ejemplo de Login',
            value={
                'username': 'usuario@ejemplo.com',
                'password': 'contraseña123'
            },
            request_only=True,
        ),
    ]
)
def login(request):
    # ...
```

## 🔍 Filtros y Búsqueda

La API soporta filtrado, búsqueda y ordenamiento:

```
GET /api/v1/shop/products/?category=1&search=arroz&ordering=-price
```

Estos parámetros se documentan automáticamente en Swagger UI.

## 📦 Exportar Documentación

### Generar archivo OpenAPI

```bash
python manage.py spectacular --file schema.yml
```

### Generar documentación estática

```bash
python manage.py spectacular --file schema.yml --format openapi-json
```

## 🌐 Producción

En producción, considera:

1. **Deshabilitar Swagger UI** si no es necesario:
   ```python
   # settings.py
   SPECTACULAR_SETTINGS = {
       'SERVE_PUBLIC': False,  # Solo para usuarios autenticados
   }
   ```

2. **Cachear el schema**:
   ```python
   SPECTACULAR_SETTINGS = {
       'SERVE_INCLUDE_SCHEMA': False,
   }
   ```

3. **Servir documentación estática** con Nginx/Apache

## 📚 Recursos Adicionales

- [Documentación oficial drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

*Última actualización: 2025-11-25*

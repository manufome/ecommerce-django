# Mi Tienda — Backend API

API RESTful para la plataforma de e-commerce **Mi Tienda**, construida con Django y Django Rest Framework.

**Live Demo:** [https://web-production-b62672.up.railway.app](https://web-production-b62672.up.railway.app)
**Swagger Docs:** [https://web-production-b62672.up.railway.app/api/docs/](https://web-production-b62672.up.railway.app/api/docs/)

## Características

- **JWT Authentication** — login, registro, refresh token, blacklist
- **Product Catalog** — productos, categorías (MPTT), marcas, imágenes
- **Order System** — pedidos, direcciones, pagos, cupones, reembolsos
- **Filtering** — filtros por categoría, marca, precio, novedades, búsqueda
- **Pagination** — paginación LimitOffset con 25 items por página
- **Admin Panel** — Django Jazzmin con interfaz personalizada

## Tech Stack

| Componente | Tecnología |
|------------|------------|
| Framework | Django 5.0 + DRF 3.15 |
| Base de datos | PostgreSQL (producción) / SQLite (desarrollo) |
| Autenticación | JWT via djangorestframework-simplejwt |
| Documentación | drf-spectacular (OpenAPI/Swagger) |
| Categorías | django-mptt (árbol jerárquico) |
| Filtros | django-filter |
| CORS | django-cors-headers |
| Deploy | Railway + Gunicorn |

## Estructura

```
apps/
├── users/        # Autenticación, perfiles, JWT
├── shop/         # Productos, categorías, marcas, imágenes
├── orders/       # Pedidos, direcciones, pagos, cupones
├── payments/     # Lógica de pagos
├── shipping/     # Costos y gestión de envíos
├── search/       # Búsqueda
└── shopmaster/   # Panel de administración
```

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login/` | Obtener tokens JWT |
| POST | `/api/v1/auth/login/refresh/` | Refrescar token |
| POST | `/api/v1/auth/register/` | Registrar usuario |
| GET | `/api/v1/auth/user/` | Perfil del usuario |
| GET | `/api/v1/shop/home/` | Datos de la página principal |
| GET | `/api/v1/shop/products/` | Lista de productos con filtros |
| GET | `/api/v1/shop/products/:slug/` | Detalle de producto |
| GET | `/api/v1/shop/categories/` | Árbol de categorías |
| GET | `/api/v1/shop/brands/` | Lista de marcas |
| GET | `/api/v1/orders/choices/` | Opciones de dirección/pago |
| POST | `/api/v1/orders/orders/` | Crear pedido |
| GET | `/api/v1/orders/addresses/` | Direcciones del usuario |
| GET | `/api/docs/` | Swagger UI |

## Instalación Local

### Prerrequisitos
- Python 3.12+
- PostgreSQL (opcional — SQLite funciona para desarrollo)

### Pasos

```bash
# Clonar
git clone https://github.com/manufome/ecommerce-django.git
cd ecommerce-django

# Entorno virtual
python3.12 -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Migraciones
python manage.py migrate

# Superusuario
python manage.py createsuperuser

# Poblar datos de ejemplo
python manage.py init_data

# Servidor
python manage.py runserver
```

La API estará en `http://localhost:8000`.
Swagger docs en `http://localhost:8000/api/docs/`.

### Variables de Entorno

| Variable | Descripción |
|----------|-------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `True` en desarrollo, `False` en producción |
| `ALLOWED_HOSTS` | Dominios permitidos (ej: `localhost,127.0.0.1`) |
| `DB_URL` | URL de conexión a la base de datos |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS |

## Despliegue

El proyecto incluye configuración para **Railway**:
- `Procfile` — ejecuta migraciones, seed data, y gunicorn
- `runtime.txt` — especifica Python 3.12
- `whitenoise` — sirve archivos estáticos en producción

## Autor

**Manuel Forero** — Junior Web Developer

- GitHub: [@manufome](https://github.com/manufome)
- LinkedIn: [Manuel Forero](https://linkedin.com/in/manuel-forero)

---

Backend del proyecto [Mi Tienda Frontend](https://github.com/manufome/ecommerce-react).

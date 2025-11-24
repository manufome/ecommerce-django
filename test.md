# Tests Documentation (test.md)

## Overview
Este proyecto incluye **5 tests automatizados** que cubren los aspectos críticos de la API:
- Autenticación y autorización (registro, login, rutas protegidas).
- Home page data aggregation (productos destacados, en oferta, etc.).
- Creación de órdenes y gestión de stock.

## Cómo ejecutar los tests
```bash
# Activar el entorno virtual (si no está activado)
.\venv\Scripts\activate

# Ejecutar con salida detallada
.\venv\Scripts\python.exe manage.py test tests --verbosity 2
```

## Lista de tests y lo que verifican
| Archivo | Test | Endpoint | Entrada (JSON) | Resultado esperado |
|--------|------|----------|----------------|--------------------|
| `tests/test_auth.py` | `test_register` | `POST /api/v1/auth/register/` | `{ "username": "testuser", "email": "test@example.com", "first_name": "Test", "last_name": "User", "password": "Testpassword123!", "confirm_password": "Testpassword123!" }` | **201 Created** – nuevo `User` en la base de datos |
| | `test_login` | `POST /api/v1/auth/login/` | `{ "username": "testuser", "password": "Testpassword123!" }` | **200 OK** – tokens `access` y `refresh` |
| | `test_protected_route` | `GET /api/v1/auth/user/` (con header `Authorization: Bearer <access>` ) | — | **200 OK** – datos del usuario autenticado |
| `tests/test_shop.py` | `test_home_data` | `GET /api/v1/shop/home/` | — | **200 OK** – estructura JSON con `best_selling`, `featured`, `latest`, `on_sale` y datos correctos de cada producto |
| `tests/test_orders.py` | `test_create_order` | `POST /api/v1/orders/` | ```json
{ "address": { "first_name": "Test", "last_name": "User", "email": "test@example.com", "phone": "1234567890", "locality": "CHA", "street_type": "CL", "street_value": "79a", "number": "123", "complement": "Apt 401" }, "products": [{ "product_id": 1, "qty": 2 }], "payment_method": "CE", "notes": "" }
``` | **201 Created** – orden guardada y **stock del producto decrementado** |

## Salida típica (verbosity 2)
```
test_login (tests.test_auth.AuthTests)                     ... ok
test_protected_route (tests.test_auth.AuthTests)          ... ok
test_register (tests.test_auth.AuthTests)                ... ok
test_create_order (tests.test_orders.OrderTests)         ... ok
test_home_data (tests.test_shop.ShopTests)               ... ok

----------------------------------------------------------------------
Ran 5 tests in 1.33s

OK
```
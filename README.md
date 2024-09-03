# Proyecto de Comercio Electrónico Django

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

Este es un proyecto de comercio electrónico desarrollado con Django y Django Rest Framework.

## Aplicaciones

El proyecto consta de las siguientes aplicaciones principales:

1. **Shop**: Gestiona productos, categorías y marcas.
2. **Orders**: Maneja los pedidos de los clientes.
3. **Cart**: Administra el carrito de compras.
4. **Payments**: Procesa los pagos de los pedidos.
5. **Shipping**: Gestiona el envío de los productos.
6. **Search**: Proporciona funcionalidad de búsqueda de productos.
7. **Users**: Maneja la autenticación y los perfiles de usuario.

## Características principales

-   API RESTful completa
-   Autenticación JWT
-   Filtrado, búsqueda y ordenación de productos
-   Gestión de carrito de compras
-   Procesamiento de pedidos y pagos
-   Sistema de envíos
-   Perfiles de usuario y listas de deseos

## Configuración del proyecto

1. Clona el repositorio
2. Crea un entorno virtual y actívalo
3. Instala las dependencias: `pip install -r requirements.txt`
4. Configura la base de datos en `config/settings.py`
5. Aplica las migraciones: `python manage.py migrate`
6. Crea un superusuario: `python manage.py createsuperuser`
7. Ejecuta el servidor: `python manage.py runserver`

## API Documentation

La documentación de la API está disponible en formato Swagger. Puedes acceder a ella en la ruta `/docs/` una vez que el servidor esté en funcionamiento.

## Licencia

Este proyecto está bajo la Licencia Apache 2.0. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir cambios o mejoras.

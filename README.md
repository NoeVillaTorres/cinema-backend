# Cinema Catalog — Backend

API REST desarrollada con FastAPI y PostgreSQL para la gestión de un catálogo de películas y series.

Este proyecto forma parte de una evaluación técnica de desarrollo de software para Turing Inteligencia Artificial.

## 1. Descripción

Cinema Catalog es una aplicación web que permite explorar un catálogo de películas y series, consultar información detallada y administrar los títulos registrados.

El backend proporciona una API REST que permite al frontend consultar los datos y realizar operaciones administrativas.

Incluye autenticación mediante JWT y autorización basada en dos roles: `admin` y `user`.

El proyecto está orientado a una demostración funcional de desarrollo full-stack, con énfasis en organización del código, validación de datos, persistencia y seguridad básica.

## 2. Tecnologías utilizadas

| Tecnología | Propósito |
|---|---|
| Python 3.13.5 | Lenguaje de programación |
| FastAPI | Desarrollo de la API REST |
| PostgreSQL 16 | Base de datos relacional |
| SQLAlchemy 2 | ORM y operaciones con la base de datos |
| Pydantic 2 | Validación y serialización de datos |
| Psycopg | Conexión entre Python y PostgreSQL |
| PyJWT | Generación y validación de tokens JWT |
| pwdlib y Argon2 | Hash y verificación de contraseñas |
| python-dotenv | Carga de variables de entorno |
| Uvicorn | Servidor ASGI |

Las versiones completas de las dependencias de Python se encuentran en `requirements.txt`.

## 3. Funcionalidades principales

### Consulta del catálogo

- Obtener películas y series.
- Buscar títulos por nombre.
- Filtrar por tipo: película o serie.
- Filtrar por género.
- Consultar los detalles de un título.
- Obtener los géneros disponibles.

### Administración

Los usuarios con rol `admin` pueden:

- Registrar nuevos títulos.
- Modificar títulos existentes.
- Eliminar títulos.

### Autenticación y autorización

- Inicio de sesión mediante correo electrónico y contraseña.
- Generación de tokens JWT.
- Consulta del usuario autenticado.
- Restricción de operaciones administrativas según el rol.

## 4. Estructura del proyecto

```text
cinema-backend/
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── genres.py
│   └── titles.py
├── auth.py
├── create_user.py
├── database.py
├── init_db.py
├── main.py
├── models.py
├── requirements.txt
├── schemas.py
└── seed.py
```

### Responsabilidades de los archivos

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Inicialización de FastAPI, configuración de CORS y registro de rutas |
| `database.py` | Conexión a PostgreSQL y gestión de sesiones |
| `models.py` | Modelos SQLAlchemy y relaciones entre tablas |
| `schemas.py` | Validación de solicitudes y serialización de respuestas |
| `auth.py` | Hash de contraseñas, JWT y autorización |
| `routes/auth.py` | Endpoints de autenticación |
| `routes/titles.py` | Consultas y CRUD de títulos |
| `routes/genres.py` | Consulta de géneros |
| `init_db.py` | Creación inicial de tablas |
| `seed.py` | Carga de datos de demostración |
| `create_user.py` | Creación de cuentas desde la terminal |

Esta separación permite mantener las responsabilidades del proyecto organizadas sin introducir capas innecesarias.

## 5. Requisitos previos

Para ejecutar el backend localmente se necesita:

- Python 3.13.5 o una versión compatible con las dependencias.
- PostgreSQL 16 o una versión compatible.
- `pip`.
- Acceso a una terminal.

El desarrollo se realizó en Ubuntu.

## 6. Instalación

### 6.1. Clonar el repositorio

```bash
git clone https://github.com/NoeVillaTorres/cinema-backend
cd cinema-backend
```


### 6.2. Crear un entorno virtual

```bash
python3 -m venv .venv
```

Activarlo en Linux:

```bash
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 6.3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## 7. Configuración de PostgreSQL

El proyecto utiliza una base de datos PostgreSQL local.

En Ubuntu, acceder a PostgreSQL con el usuario administrador:

```bash
sudo -u postgres psql
```

Crear un usuario para la aplicación:

```sql
CREATE USER cinema_user WITH PASSWORD 'CONTRASENA_LOCAL';
```

Crear la base de datos:

```sql
CREATE DATABASE cinema_db OWNER cinema_user;
```

Salir de PostgreSQL:

```sql
\q
```

Los nombres `cinema_user` y `cinema_db` son ejemplos de configuración local.

Si se utilizan otros nombres, deben reflejarse en la variable `DATABASE_URL`.

## 8. Variables de entorno

En la raíz del backend, crear un archivo llamado `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://cinema_user:CONTRASENA_LOCAL@localhost:5432/cinema_db
JWT_SECRET_KEY=CLAVE_SECRETA_ALEATORIA
```

### Descripción de las variables

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL |
| `JWT_SECRET_KEY` | Clave utilizada para firmar y validar los tokens JWT |

La clave JWT debe ser aleatoria y suficientemente larga.

Puede generarse con Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

El archivo `.env` contiene información privada y no debe incluirse en Git.

**Importante:** reemplazar los valores de ejemplo antes de ejecutar el proyecto.

## 9. Inicialización de la base de datos

Una vez configuradas las variables de entorno, ejecutar los siguientes comandos desde la carpeta `cinema-backend`.

### 9.1. Crear las tablas

```bash
python init_db.py
```

Este script utiliza los modelos SQLAlchemy para crear las tablas que todavía no existan.

No modifica automáticamente la estructura de tablas existentes ni funciona como un sistema de migraciones.

### 9.2. Cargar datos de demostración

```bash
python seed.py
```

El script registra los géneros y títulos utilizados como datos iniciales del catálogo.

**Nota:** al ejecutarse nuevamente, el script puede actualizar datos de los títulos de demostración existentes. Se recomienda utilizarlo durante la preparación inicial de la base de datos.

### 9.3. Crear una cuenta

```bash
python create_user.py
```

El script solicita los datos necesarios para crear un usuario, incluida su contraseña.

Para probar las funciones administrativas se requiere una cuenta con rol `admin`.

También puede crearse una cuenta con rol `user` para verificar las restricciones de acceso.

Las contraseñas se almacenan mediante hash; no se guardan en texto plano.

## 10. Ejecución del servidor

Iniciar FastAPI con Uvicorn:

```bash
uvicorn main:app --reload
```

El backend estará disponible en:

```text
http://localhost:8000
```

El parámetro `--reload` permite reiniciar el servidor automáticamente cuando cambia el código durante el desarrollo.

### Documentación interactiva

FastAPI genera documentación interactiva de la API:

**Swagger UI:**

```text
http://localhost:8000/docs
```

**OpenAPI:**

```text
http://localhost:8000/openapi.json
```

Desde Swagger UI se pueden consultar los esquemas, enviar solicitudes y comprobar las respuestas de los endpoints.

## 11. Endpoints de la API

### Consulta pública

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/titles` | Consultar el catálogo |
| GET | `/titles/{id}` | Obtener los detalles de un título |
| GET | `/genres` | Consultar los géneros disponibles |

### Autenticación

| Método | Endpoint | Descripción | Acceso |
|---|---|---|---|
| POST | `/auth/login` | Iniciar sesión y obtener un JWT | Público |
| GET | `/auth/me` | Consultar el usuario autenticado | Autenticado |

### Administración de títulos

| Método | Endpoint | Descripción | Acceso |
|---|---|---|---|
| POST | `/titles` | Crear un título | Administrador |
| PUT | `/titles/{id}` | Actualizar un título | Administrador |
| DELETE | `/titles/{id}` | Eliminar un título | Administrador |

### Filtros disponibles

`GET /titles` admite los siguientes parámetros de consulta:

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `search` | Buscar títulos por nombre | `?search=Interstellar` |
| `type` | Filtrar por película o serie | `?type=movie` |
| `genre` | Filtrar por nombre de género | `?genre=Drama` |

Los filtros pueden combinarse.

Ejemplo:

```http
GET /titles?type=movie&genre=Drama
```

### Ejemplo de creación de un título

```http
POST /titles
Authorization: Bearer TOKEN_JWT
Content-Type: application/json
```

Cuerpo de ejemplo:

```json
{
  "name": "Película de ejemplo",
  "synopsis": "Descripción de una película de demostración.",
  "type": "movie",
  "release_year": 2024,
  "poster_url": null,
  "genre_ids": [1]
}
```

El identificador del género debe existir previamente en la base de datos.

La actualización mediante `PUT` utiliza los campos completos del título.

Para consultar ejemplos adicionales de solicitudes y respuestas, utilizar Swagger UI.

## 12. Modelo de datos

La base de datos contiene cuatro tablas principales:

### `users`

Almacena las cuentas registradas, las contraseñas protegidas mediante hash y los roles de acceso.

### `titles`

Almacena la información de películas y series:

- Nombre.
- Sinopsis.
- Tipo.
- Año de estreno.
- URL del póster.

### `genres`

Almacena los géneros disponibles.

Cada género se registra una sola vez para evitar repetir su información en cada título.

### `title_genres`

Tabla intermedia que representa la relación de muchos a muchos entre títulos y géneros.

Un título puede pertenecer a varios géneros y un género puede estar relacionado con varios títulos.

### Normalización

El esquema se diseñó siguiendo principios de normalización hasta la tercera forma normal (3NF):

- Los atributos almacenan valores individuales.
- Los datos de géneros se mantienen separados de los títulos.
- La relación muchos a muchos se resuelve mediante una tabla intermedia.
- Las relaciones se establecen mediante claves primarias y foráneas.

Esta estructura reduce la redundancia y facilita mantener la integridad de los datos.

## 13. Autenticación y autorización

La autenticación se realiza mediante correo electrónico y contraseña.

Después de validar las credenciales, la API genera un token JWT con tiempo de expiración.

Los endpoints protegidos esperan el token en el encabezado:

```http
Authorization: Bearer TOKEN_JWT
```

### Roles

**`admin`**

Puede consultar el catálogo y realizar las operaciones de creación, actualización y eliminación de títulos.

**`user`**

Puede autenticarse y consultar la información pública, pero no realizar operaciones administrativas.

La autorización se comprueba en el backend, independientemente de las restricciones visuales implementadas en el frontend.

### Seguridad implementada

- Hash de contraseñas con Argon2.
- Tokens JWT firmados.
- Verificación de expiración de tokens.
- Autorización basada en roles.
- Variables de entorno para credenciales y claves.
- Validación de datos mediante Pydantic.
- Consultas a PostgreSQL mediante SQLAlchemy.

## 14. Validaciones y manejo de errores

La API utiliza esquemas Pydantic para comprobar los datos recibidos.

Entre las validaciones se incluyen:

- Campos obligatorios.
- Longitud permitida del nombre.
- Contenido no vacío en nombre y sinopsis.
- Tipo de título válido: `movie` o `series`.
- Año de estreno dentro del rango permitido.
- Selección de al menos un género.
- Comprobación de identificadores de género existentes.

La API utiliza códigos HTTP para comunicar los resultados de las solicitudes.

| Código | Significado |
| ---|---|
| `200 OK` | Consulta, actualización o autenticación correcta |
| `201 Created` | Título creado correctamente |
| `204 No Content` | Título eliminado correctamente |
| `401 Unauthorized` | Credenciales o token inválidos |
| `403 Forbidden` | Usuario sin permisos de administrador |
| `404 Not Found` | Título inexistente |
| `422 Unprocessable Entity` | Datos que no cumplen las validaciones |

Los esquemas y respuestas exactos de cada endpoint pueden consultarse en Swagger UI.

## 15. Integración con el frontend

El backend está diseñado para comunicarse con el frontend de Cinema Catalog, desarrollado con React.

La API utiliza JSON para intercambiar información.

Durante el desarrollo local, el frontend se ejecuta normalmente en:

```text
http://localhost:5173
```

Y el backend en:

```text
http://localhost:8000
```

FastAPI configura CORS para permitir las solicitudes desde los orígenes locales definidos en la aplicación.

Repositorio del frontend:

**[Cinema Catalog — Frontend](https://github.com/NoeVillaTorres/Cinema-frontend)**

## 16. Consideraciones y limitaciones

Cinema Catalog fue desarrollado como parte de una evaluación técnica de tiempo limitado.

Las siguientes decisiones corresponden al alcance del proyecto:

- El sistema está orientado a la ejecución local.
- El catálogo utiliza datos iniciales de demostración.
- La creación de usuarios se realiza mediante un script de terminal.
- La inicialización de tablas se realiza mediante SQLAlchemy.
- No se implementó un sistema de migraciones.
- La autenticación utiliza tokens JWT con expiración.
- El proyecto no implementa reproducción de contenido audiovisual.

El objetivo es demostrar una implementación funcional y comprensible de una API REST con persistencia, validación de datos y control básico de acceso.

## 17. Autor

Proyecto desarrollado como parte del periodo de evaluación técnica para el puesto Trainee de Desarrollo de Software en Turing Inteligencia Artificial.

**Fecha:** octubre de 2026.

## Repositorios

Cinema Catalog está dividido en dos repositorios independientes:

- [Backend — FastAPI y PostgreSQL](https://github.com/NoeVillaTorres/cinema-backend)
- [Frontend — React y Vite](https://github.com/NoeVillaTorres/Cinema-frontend)
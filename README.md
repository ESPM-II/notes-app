Proyecto Notes Backend

Este es un backend desarrollado en Python con FastAPI y PostgreSQL como base de datos. Al ejecutar la aplicación, las tablas se crean automáticamente.

Requisitos previos:

Instalación de PostgreSQL

Descarga e instala PostgreSQL desde https://www.postgresql.org/download/.

Durante la instalación, utilizar el usuario por defecto postgres.

Configura la contraseña del usuario postgres como Db2025!.

Crea una base de datos llamada note_app.

Configuración del entorno virtual

Crear el entorno virtual

python -m venv venv

Activar el entorno virtual

En Windows:

venv\Scripts\activate

En macOS/Linux:

source venv/bin/activate

Instalar dependencias

pip install -r requirements.txt

Configuración del entorno

Crear archivo .env en el directorio del proyecto con la siguiente configuración:

SECRET_KEY=k9dB2W6xHqF8GzK1mYJ7aT0LpRfXqC3V
ALGORITHM=HS256
DATABASE_URL=postgresql://postgres:Db2025!@localhost/note_app

Ejecución de la aplicación

Una vez configurado todo, ejecuta el servidor con Uvicorn:

uvicorn app.main:app --reload

La API estará disponible en:

http://127.0.0.1:8000

Creación automática de tablas

Cuando la aplicación se ejecuta por primera vez, las tablas de la base de datos se crean automáticamente. No es necesario ejecutar migraciones manualmente.

Endpoints y documentación

FastAPI genera automáticamente documentación interactiva accesible en:

Swagger UI: http://127.0.0.1:8000/docs

¡IMPORTANTE!

Es importante que la contraseña de PostgreSQL sea Db2025! para evitar problemas de conexión.

Si poseen otra configuración de base de datos, actualizar el archivo .env y asegurarse de modificar la cadena de conexión (DATABASE_URL).

Autor

Desarrollado por Juan José Alegría.


# Bot Hispanic Python

Este es un bot de Discord desarrollado en Python que incluye varias funcionalidades de moderación y administración para servidores de Discord.

## Características

- **Banear Usuarios:** Permite a los owners de servidores banear usuarios con una razón y una fecha de finalización del baneo.
- **Desbanear Usuarios:** Permite a los owners de servidores desbanear usuarios.
- **Añadir Owners:** Permite a los owners de servidores añadir otros owners/moderadores a su servidor.
- **Quitar Owners:** Permite a los owners de servidores eliminar otros owners/moderadores de su servidor.
- **Listar Owners:** Lista todos los owners del servidor.
- **Listar Servidores:** Lista todos los servidores en los que está el bot, obtenidos de la base de datos SQLite.
- **Listar Acciones de Moderadores:** Lista todas las acciones realizadas por un moderador en un servidor específico.
- **Cambiar Color de Roles:** Cambia el color de un rol cada segundo durante dos minutos.
- **Mutear Usuarios:** Permite a los owners de servidores mutear usuarios por un periodo de tiempo específico.
- **Desmutear Usuarios:** Permite a los owners de servidores desmutear usuarios.
- **Advertir Usuarios:** Permite a los moderadores advertir a los usuarios por comportamientos inapropiados.
- **Desadvertir Usuarios:** Permite a los moderadores desadvertir a los usuarios.
- **Expulsar Usuarios:** Permite a los moderadores expulsar a los usuarios del servidor.
- **Limpiar Mensajes:** Permite a los moderadores eliminar un número específico de mensajes en un canal.
- **Establecer Canal de Logs y rol de cuarentena:** Permite a los administradores establecer un canal donde se registren todas las acciones de moderación además de añadir un rol de cuarentena.
- **Ver Información del Usuario:** Permite a los usuarios ver información detallada sobre un miembro del servidor.
- **Ver Información del Servidor:** Permite a los usuarios ver información detallada sobre el servidor.
- **Poner en Cuarentena:** Permite a los owners de servidores poner a un usuario en cuarentena, asignándole un rol especial sin permisos.
- **Sacar de Cuarentena:** Permite a los owners de servidores sacar a un usuario de cuarentena.
- **Verificación de Sanciones:** Verifica periódicamente las sanciones y las elimina cuando llega la fecha límite.
- **Verificación de Creación de tickets:** Verifica periódicamente si algún ticket es creado y menciona a los roles correspondientes dentro del propio ticket.
- **Enviar Mensaje Directo a Rol:** Permite enviar un mensaje directo a todos los miembros con un rol específico.
- **Buscar Juego:** Permite buscar información sobre un juego en la base de datos de RAWG.
- **Pregunta a la IA:** Permite hacer preguntas a una IA y obtener respuestas generadas por un modelo de lenguaje.
- **Generar Imagen con IA:** Permite generar una imagen a partir de un texto utilizando un modelo de IA.
- **Añadir Sticker:** Permite añadir un sticker al servidor.
- **Mostrar Comandos Disponibles:** Muestra una lista de todos los comandos disponibles y su descripción.

## Requisitos

- Python 3.8+
- Discord.py
- SQLite3
- dotenv

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/Z4NO/BOT-DISCORD-HISPANIC
    cd bot-hispanic-python
    ```

2. Crea un entorno virtual y actívalo:
    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Crea un archivo [`.env`](.env ) en el directorio raíz del proyecto y añade tu token de Discord:
    ```env
    DISCORD_TOKEN=tu_token_de_discord
    DISCORD_GUILD=tu_id_de_guild
    RAWG_API_KEY=tu_rawg_api_key
    HUGGINGFACE_TOKEN=tu_huggingface_token
    ```

5. Ejecuta el script para crear la base de datos SQLit

## Uso

Para iniciar el bot, simplemente ejecuta el archivo [`main.py`](main.py ):
```sh
python main.py

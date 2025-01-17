# Bot Hispanic Python

Este es un bot de Discord desarrollado en Python que incluye varias funcionalidades de moderación y administración para servidores de Discord.

## Características

- **Banear Usuarios:** Permite a los owners de servidores banear usuarios con una razón y una fecha de finalización del baneo.
- **Desbanear Usuarios:** Permite a los owners de servidores desbanear usuarios.
- **Añadir Owners:** Permite a los owners de servidores añadir otros owners/moderadores a su servidor.
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
- **Verificación de Sanciones:** Verifica periódicamente las sanciones y las elimina cuando llega la fecha límite.
- **Verificación de Creación de tickets:** Verifica periódicamente si algún ticket es creado y meciona a los roles correspondiente dentro del propio ticket.

## Requisitos

- Python 3.8+
- Discord.py
- SQLite3
- dotenv

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu_usuario/bot-hispanic-python.git
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
    ```

5. Ejecuta el script para crear la base de datos SQLite (si no la tienes ya):
    ```sh
    python create_db.py
    ```

## Uso

Para iniciar el bot, simplemente ejecuta el archivo [`main.py`](main.py ):
```sh
python main.py

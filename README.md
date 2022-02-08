# chat-broadcast

Una herramienta para transmitir mensajes automáticamente a múltiples grupos de chat

# Setup

## Librerías

Necesitas Python 3 con la librería `python-dotenv` y `python-telegram-bot` instaladas. Para instalarlas basta con ejecutar:

```
pip3 install -r requirements.txt
```

## Matterbridge

### Descargar ejecutable

Debes descargar el ejecutable de matterbrigde (preferentemente versión 1.23.2) correspondiente a tu sistema operativo. Puedes buscarlo [aquí](https://github.com/42wim/matterbridge/releases).

### Configuración

Tanto en el archivo `basefile.toml` como en `searchgroups.toml` debes ingresar el número de teléfono a utilizar en la línea 4. Te debe quedar algo de la forma:

```
Number="+56912345678"
```

Ejecuta una vez el archivo descargado en el paso anterior con los siguientes argumentos:

```
./[EXECUTABLE_FILENAME] -conf searchgroups.toml
```

Donde `[EXECUTABLE_FILENAME]` corresponde al nombre del archivo ejecutable. Por ejemplo, `matterbridge-1.23.2-linux-64bit`.

Esto te entregará varias cosas, entre ellas una lista de `ids` de grupos de WhatsApp con la forma `123456789123456789@g.us`. Elige el id correspondiente al grupo destinado al envío de mensajes (wid_input) y guardalo en alguna parte, lo necesitarás más adelante.

## Env file

Debes crear un archivo de nombre `.env` en la raíz del repositorio. Este archivo debe contener:

```
# main.py
BOT_NAME=[NOMBRE_BOT]
CMD=matterbridge -conf matterbridge.toml
TOKEN=[TELEGRAM_BOT_TOKEN]
CHAT_ID=[TELEGRAM_CHAT_ID]

# generator.py
EXECUTABLE=matterbridge-1.23.2-darwin-64bit
WID_INPUT=123456789123456789@g.us
```

Las diferentes variables servirán para diferentes módulos. El primer conjunto de variables solo es utilizado en `main.py`, mientras que el segundo conjunto solo es utilizado en `generator.py`.

## matterbridge.toml

Para utilizar Matterbridge, primero debes configurar un archivo `toml` adecuado. Puedes ver la documentación en detalle de este archivo [aquí](https://github.com/42wim/matterbridge/wiki/How-to-create-your-config).

Opcionalmente, el módulo `generator.py` te ayuda a generar un archivo `matterbridge.toml` básico. Para ello solo debes ejecutar:

```
python3 generator.py -n "[NOMBRE]"
```

Donde el parámetro `-n` nos permite filtrar los grupos deseados según su nombre. En `[NOMBRE]` debemos añadir una frase común contenida en todos los nombres de los grupos de llegada. Este parámetro es opcional, por lo que si ejecutas `python3 main.py` simplemente no se aplicará el filtro.

Esto generará un archivo `matterbridge.toml` con todos los grupos de WhatsApp en los cuales el número de teléfono ingresado anteriormente forme parte y cumplan con el filtro indicado en el parámetro `-n`.

Además puedes dejar corriendo `generator.py` y el programa funcionará normalmente, con la particularidad de que `matterbridge.toml` se actualizará una vez al día con los grupos en que el número ha sido agregado.

# Ejecución

Con todo lo anterior ya configurado, solo debes ejecutar:

```
python3 main.py --cmd "[COMANDO_A_EJECUTAR]"
```

Donde el parámetro opcional `--cmd` nos permite ejecutar un comando distinto al indicado en `.env`. En caso de que el comando no sea especificado ni como argumento ni como variable de entorno, se utilizará el comando por defecto:

```
/usr/bin/matterbridge -conf /etc/bot/matterbridge.toml
```

Este archivo ejecutará el comando indicado. En caso de que ocurra un error y la ejecución del comando finalice, el programa esperará 10 minutos y realizará una nueva ejecución del comando. Para finalizar definitivamente el programa se debe presionar Ctrl+C.

Se enviarán notificaciones cuando comience la ejecución del comando, en la espera para realizar una nueva ejecución y cuando el programa finalice definitivamente. Estas notificaciones serán enviadas al chat de Telegram especificado por su id y token del bot `.env` por medio de las variables de entorno `TOKEN` y `CHAT_ID` respectivamente.

## Blacklist

En un archivo `blacklist.txt` ubicado en el directorio raíz puedes agregar los WIDs de grupos que en ningún caso quieres considerar al momento de generar un archivo `matterbridge.toml` con `generator.py`. Añádelos de la forma:

``
123456789123456789@g.us
234567891234567891@g.us
...

```

# Referencias

- Para más información sobre el funcionamiento de matterbridge, puedes revisar [su documentación](https://github.com/42wim/matterbridge).
```

- Para más información del Wrapper de Telegram utilizado, revisar [su documentación](https://github.com/python-telegram-bot/python-telegram-bot).

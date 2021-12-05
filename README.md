# chat-broadcast
Una herramienta para transmitir mensajes automáticamente a múltiples grupos de chat

# Setup

## Librerías
Necesitas Python 3 con la librería `python-dotenv` instalada. Para instalarla basta con ejecutar:
```
pip3 install -r requirements.txt
```

## Matterbridge
### Descargar ejecutable
Debes descargar el ejecutable de matterbrigde (preferentemente versión 1.32.2) correspondiente a tu sistema operativo. Puedes buscarlo [aquí](https://github.com/42wim/matterbridge/releases/tag/v1.23.2).

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
EXECUTABLE=matterbridge-1.23.2-linux-64bit
WID_INPUT=123456789123456789@g.us
```
Siendo el primer valor el nombre del ejecutable correspondiente a tu sistema operativo y el segundo valor el id del grupo destinado al envío de mensajes.

# Ejecución

Con todo lo anterior ya configurado, solo debes ejecutar:
```
python3 main.py -n "[NOMBRE]"
```
Donde el parámetro `-n` nos permite filtrar los grupos deseados según su nombre. En `[NOMBRE]` debemos añadir una frase común contenida en todos los nombres de los grupos de llegada. Este parámetro es opcional, por lo que si ejecutas ``python3 main.py` simplemente no se aplicará el filtro.

## Blacklist

En un archivo `blacklist.txt` ubicado en el directorio raíz puedes agregar los WIDs de grupos que en ningún caso quieres considerar. Añádemos de la forma:

``
123456789123456789@g.us
234567891234567891@g.us
...

```

# Referencias

- Para más información sobre el funcionamiento de matterbridge, puedes revisar [su documentación](https://github.com/42wim/matterbridge).

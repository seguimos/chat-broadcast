import os
import time
import builtins
from datetime import datetime as dt
from dotenv import load_dotenv


# Variables de entorno
load_dotenv()
wid_input = os.getenv('WID_INPUT')
executable = os.getenv('EXECUTABLE')

# Constantes
tomlFilename = "matterbridge.toml"
waittime = 30*60
matterbrige_cmd = f'./{executable} -conf {tomlFilename}'


def print(*args, **kwargs):
    now = f'[{dt.now().strftime("%m-%d-%Y %H:%M:%S")}]'
    return builtins.print(now, *args, **kwargs)


if __name__ == "__main__":
    while True:
        print(f"Ejecutando {tomlFilename}...")
        os.system(matterbrige_cmd)

        print(
            f"Ejecución detenida. Esperando {waittime/60:.0f} minutos para reanudar...")
        print("Presiona Ctrl+C para detener definitivamente.")
        time.sleep(waittime)

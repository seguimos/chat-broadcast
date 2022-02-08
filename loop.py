import os
import time
import builtins
import argparse
from datetime import datetime as dt
from dotenv import load_dotenv
from notifier import send_message


# Argumentos
parser = argparse.ArgumentParser(description='Ejecuta un comando en loop.')
parser.add_argument('-c', '--cmd', type=str,
                    help='Ingresa el comando a ejecutar')
args = parser.parse_args()

# Constantes
WAITTIME = 10*60
DEFAULT_CMD = "/usr/bin/matterbridge -conf /etc/bot/matterbridge.toml"

# Variables de entorno
load_dotenv()
bot_name = os.getenv('BOT_NAME')
if args.cmd:
    cmd = args.cmd
else:
    cmd = os.getenv('CMD', default=DEFAULT_CMD)
token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')


def print(*args, **kwargs):
    now = f'[{dt.now().strftime("%m-%d-%Y %H:%M:%S")}]'
    return builtins.print(now, *args, **kwargs)


if __name__ == "__main__":
    try:
        while True:
            print(f"Ejecutando: {cmd}...")
            send_message(f"✅ Ejecutando {bot_name}...", token, chat_id)
            os.system(cmd)

            print(
                f"Ejecución detenida. Esperando {WAITTIME/60:.0f} minutos para reanudar...")
            print("Presiona Ctrl+C para detener definitivamente.")
            send_message(
                f"🚨 A ocurrido un error en {bot_name}. Esperando {WAITTIME/60:.0f} minutos para reanudar...",
                token, chat_id
            )
            time.sleep(WAITTIME)
    except:
        print(f"Loop terminado")
        send_message(
            f"❌ {bot_name} detenido", token, chat_id)
        exit()

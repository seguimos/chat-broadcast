import os
import time
import signal
import logging
import builtins
import argparse
from datetime import datetime as dt
from dotenv import load_dotenv
from telegram.ext import Updater


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


# Telegram
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token=token, use_context=True)
bot = updater.bot


def print(*args, **kwargs):
    now = f'[{dt.now().strftime("%m-%d-%Y %H:%M:%S")}]'
    return builtins.print(now, *args, **kwargs)


def exit_handler(*args):
    print(f"Loop terminado")
    bot.send_message(chat_id, f"❌ {bot_name} detenido")
    exit()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, exit_handler)

    while True:
        print(f"Ejecutando: {cmd}...")
        bot.send_message(chat_id, f"✅ Ejecutando {bot_name}")
        a = os.system(cmd)
        print(a)

        print(
            f"Ejecución detenida. Esperando {WAITTIME/60:.0f} minutos para reanudar...")
        print("Presiona Ctrl+C para detener definitivamente.")
        bot.send_message(
            chat_id,
            f"🚨 A ocurrido un error en {bot_name}. Esperando {WAITTIME/60:.0f} minutos para reanudar."
        )
        try:
            time.sleep(WAITTIME)
        except KeyboardInterrupt:
            exit_handler()

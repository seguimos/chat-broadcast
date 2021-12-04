import os
import subprocess
from dotenv import load_dotenv




load_dotenv()

wid_input  = os.getenv('WID_INPUT')
executable = os.getenv('EXECUTABLE')

logFilename    = "output.txt"
searchFilename = "searchgroups.toml"
baseFilename   = "basefile.toml"
tomlFilename   = "matterbridge.toml"
search_cmd      = f'./{executable} -conf {searchFilename} > {logFilename}'
matterbrige_cmd = f'./{executable} -conf {tomlFilename}'



# Genera un bridge-in con el wid entregado
def generate_in(wid):
    return f'''

# 0
[[gateway.in]]
account="whatsapp.mywhatsapp"
channel="{wid}"
'''

# Genera un bridge-out con el wid entregado
def generate_out(wid, i):
    return f'''
# {i}
[[gateway.out]]
account="whatsapp.mywhatsapp"
channel="{wid}"
'''

# Genera un archivo toml con los wids entregados
def generate_toml(wid_input, wids_output, basefile=baseFilename, outfile=tomlFilename):
    content = ""
    with open(basefile, 'r') as file:
        content += file.read()
    content += generate_in(wid_input)
    for i, wid in enumerate(wids_output):
        content += generate_out(wid, i+1)
    with open(outfile, 'w') as file:
        file.write(content)
    return content




if __name__ == "__main__":
    wids_output = set()

    while True:
        print("Actualizando grupos...")
        os.system(search_cmd)
        with open(logFilename, 'r') as file:
            actual_wids = set()
            lines = file.readlines()
            for line in lines:
                if "@g.us" in line:
                    # Se accede al whatsapp id (wid)
                    wid = line.split(' ')[2].split('"')[1]
                    # Se añade el wid al set
                    actual_wids.add(wid)
        
        actual_wids.discard(wid_input)
        print(f"Se han encontrado {len(actual_wids)} grupos!")
        generate_toml(wid_input, actual_wids)

        # Ejecuta la configuración por 1 hora
        print("Ejecutando la configuración por 1 hora...")
        p = subprocess.Popen(matterbrige_cmd.split())
        try:
            p.wait(60*60)
        except subprocess.TimeoutExpired:
            p.kill()
        
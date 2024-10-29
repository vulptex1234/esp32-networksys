import os
import re

FLAG_FILE = 'flag.txt'
ENERGY_FILE = 'cumulative_energy.txt'

def file_exists(filename):
    try:
        # ファイルのステータスを取得
        os.stat(filename)
        return True
    except OSError:
        return False

# Trueに書き換え
if file_exists(FLAG_FILE):
    with open(FLAG_FILE, 'r') as f:
        flag = f.read()

    flag = flag.replace("True","False")
    with open(FLAG_FILE, 'w') as f:
        f.write(flag)

if file_exists(ENERGY_FILE):
    with open(ENERGY_FILE, 'r') as f:
        energy = f.read()

    energy = re.sub("[0-9]","0", energy)
    with open(ENERGY_FILE, 'w') as f:
        f.write(energy)
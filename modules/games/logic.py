import os
import subprocess
import time

def launch_rogue():
    os.system("cls")  # Windows clear
    print("INITIALIZING RECREATION MODULE...")
    time.sleep(1.0)
    print("RECREATION CODE 001 - AXES, ARMOUR, & ALE")
    time.sleep(1.5)

    exe_path = os.path.join("games", "Axes.exe")
    subprocess.run([exe_path])

    os.system("cls")

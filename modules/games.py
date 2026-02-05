import os
import subprocess
import time

def launch_rogue():
    os.system("clear")
    print("INITIALIZING RECREATION MODULE...")
    time.sleep(1.0)
    print("RECREATION CODE 001 - ROGUE ")
    time.sleep(1.5)
    subprocess.run(["rogue"])
    os.system("clear")
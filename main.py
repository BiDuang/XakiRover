import subprocess
import os

__version__ = 'Dev-0.1.3'

try:
    os.remove("./XInput.lock")
except FileNotFoundError:
    pass

subprocess.Popen("python3 XInput.py", shell=True)
subprocess.Popen("python3 Controllor.py", shell=True)

while(input("[XakiRover] Exit by typing 'exit': ") != "exit"):
    pass

f = open("XInput.lock", "w")
f.close()

print("[XakiRover INFO] Goodbye!")

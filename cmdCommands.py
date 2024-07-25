import subprocess
import os
import threading

def run_local_server():
    # List of commands to run
    path = os.getenv("SERVER_PATH")
    commands = [
        rf"cd {path} && .venv\rose\Scripts\activate && cd ROSE-1 && python rose-server"
    ]
    if path == "":
        raise Exception("No value in path")
    return subprocess.run(commands[0], shell=True, check=True, text=True)

def start_client():
    # List of commands to run
    path = os.getenv("SERVER_PATH")
    commands = [
        rf"cd {path} && .venv\rose\Scripts\activate && cd ROSE-1 && python rose-client -s 127.0.0.1 examples\test.py"
    ]
    if path == "":
        raise Exception("No value in path")
    return subprocess.run(commands[0], shell=True, check=True, text=True)

def connect_to_server(ip="127.0.0.1"):
    path = os.getenv("SERVER_PATH")
    # List of commands to run
    commands = [
        rf"cd {path} && .venv\rose\Scripts\activate && cd ROSE-1 && python rose-client -s {ip} examples\test.py"
    ]
    if path == "":
        raise Exception("No value in path")
    for cmd in commands:
        process = subprocess.run(cmd, shell=True, check=True, text=True)

t1 = threading.Thread(target=run_local_server)
t2 = threading.Thread(target=start_client)

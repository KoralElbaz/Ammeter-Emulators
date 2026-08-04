import yaml
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime


def request_current_from_ammeter(port: int, command: bytes):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(command)
        data = s.recv(1024)

        if not data:
            raise ConnectionError("No data received")

        return float(data.decode('utf-8'))


def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)    
    
config = load_config()

def read_current(ammeter_type: str):
    ammeter = config["ammeters"][ammeter_type]
    
    value = request_current_from_ammeter(
        ammeter["port"],
        ammeter["command"].encode()
    )

    return {
        "device": ammeter_type,
        "current": round(value, 3),
        "unit": "A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

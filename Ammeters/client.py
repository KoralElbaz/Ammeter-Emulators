import yaml
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime


def request_current_from_ammeter(port: int, command: bytes, device_name: str):
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(command)
        data = s.recv(1024)
        
        if data:
            value = float(data.decode('utf-8'))

            result = {
                "device": device_name,
                "current": round(value, 3),
                "unit": "A",
                "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            print(
                f"[{result['timestamp']}] "
                f"{result['device']} | "
                f"{result['current']} {result['unit']}"
            )
            return result
        
        else:
            print("No data received.")
            return None


def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)    
    
config = load_config()

def read_current(ammeter_type: str):
    ammeter = config["ammeters"][ammeter_type]

    return request_current_from_ammeter(
        ammeter["port"],
        ammeter["command"].encode(),
        ammeter_type
    )

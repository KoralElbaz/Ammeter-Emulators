import threading
import time
import yaml

from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from Ammeters.client import request_current_from_ammeter

    
def run_greenlee_emulator():
    greenlee = GreenleeAmmeter(5000)
    greenlee.start_server()

def run_entes_emulator():
    entes = EntesAmmeter(5001)
    entes.start_server()

def run_circutor_emulator():
    circutor = CircutorAmmeter(5002)
    circutor.start_server()
    
def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)    
    
config = load_config()
def read_current(ammeter_type: str):
    ammeter = config["ammeters"][ammeter_type]

    return request_current_from_ammeter(
        ammeter["port"],
        ammeter["command"].encode()
    )

def read_current_NUM_times(ammeter_type: str, num: int):
    results = []
    for _ in range(num):
        value = read_current(ammeter_type)
        results.append(value)
        time.sleep(1)
    return results

if __name__ == "__main__":
    # Start each ammeter in a separate thread
    threading.Thread(target=run_greenlee_emulator, daemon=True).start()
    threading.Thread(target=run_entes_emulator, daemon=True).start()
    threading.Thread(target=run_circutor_emulator, daemon=True).start()

    # This section is commented out because it shouldn't work.
    # Read the README.md file as well as the source code if you need, and fix the problem.

    # Wait for the servers to start, if you have problem restarting the servers between runs try increasing sleep time.
    time.sleep(5)
    results = read_current_NUM_times("greenlee", 5)
    print("Final greenlee results:", results)
    # request_current_from_ammeter(5002, b'MEASURE_ENTES')  # Request from ENTES Ammeter
    # request_current_from_ammeter(5003, b'MEASURE_CIRCUTOR')  # Request from CIRCUTOR Ammeter

    pass

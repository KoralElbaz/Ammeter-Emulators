import threading
import time
import yaml

from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from src.analyzers.multi_device_analyzer import MultiDeviceAnalyzer

    
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



if __name__ == "__main__":
    # Start each ammeter in a separate thread
    threading.Thread(target=run_greenlee_emulator, daemon=True).start()
    threading.Thread(target=run_entes_emulator, daemon=True).start()
    threading.Thread(target=run_circutor_emulator, daemon=True).start()

    # Wait for the servers to start, if you have problem restarting the servers between runs try increasing sleep time.
    time.sleep(5)
    
    
    ammeters = ["greenlee", "entes", "circutor"]

    analyze_multiple = MultiDeviceAnalyzer(ammeters, config["sampling"]["num_measurements"], config["sampling"]["interval"])
    results = analyze_multiple.analyze()
    print(f"results:::  {results}")

    print("\n--- Analysis per device ---")
    for device, data in results.items():
        print(device, {
        k: round(v, 4) if isinstance(v, (int, float)) else v
        for k, v in data.items()
        })

    ranking = analyze_multiple.rank_by_stability(results)

    print("\n--- Stability Ranking ---")
    for i, (device, data) in enumerate(ranking, 1):
        print(f"{i}. {device} (stdev={round(data['summary']['stdev'], 4)})")
    
    analyze_multiple.visualize_all(results)
        
    
    pass

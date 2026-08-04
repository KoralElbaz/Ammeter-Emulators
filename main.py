import threading
import time
import yaml

from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from src.analyzers.multi_device_analyzer import MultiDeviceAnalyzer
from src.results.result_manager import ResultManager

    
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
    


if __name__ == "__main__":
    # Start each ammeter in a separate thread
    threading.Thread(target=run_greenlee_emulator, daemon=True).start()
    threading.Thread(target=run_entes_emulator, daemon=True).start()
    threading.Thread(target=run_circutor_emulator, daemon=True).start()

    # Wait for the servers to start, if you have problem restarting the servers between runs try increasing sleep time.
    time.sleep(5)
    
    
    config = load_config()

    ammeters = ["greenlee", "entes", "circutor"]

    analyzer = MultiDeviceAnalyzer(
        ammeters,
        config["sampling"]["num_measurements"],
        config["sampling"]["interval"]
    )

    results = analyzer.analyze()

    print("\n--- Analysis ---")
    for device, data in results.items():
        print(device, {k: v for k, v in data.items() if k != "measurements"})

    analyzer.visualize_all(results)

    ranking = analyzer.rank_by_stability(results)

    print("\n--- Ranking ---")
    for i, (device, data) in enumerate(ranking, 1):
        print(f"{i}. {device} (stdev={round(data['stdev'], 4)})")

    # 💾 Save results
    manager = ResultManager()

    metadata = {
        "devices": ammeters,
        "num_samples": config["sampling"]["num_measurements"],
        "interval": config["sampling"]["interval"]
    }

    manager.save_results(results, metadata)
    
    pass

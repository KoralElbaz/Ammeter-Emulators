import time

from Ammeters.client import read_current


class SamplingService:
    def read_current_NUM_times(self, ammeter_type: str, num: int, interval: float):
        results = []
        for _ in range(num):
            start_time = time.time() # Measurement start time
            
            value = read_current(ammeter_type)
            if value is not None:  
                results.append(value["current"])
            else:
                print(f"⚠️ Failed reading from {ammeter_type}")
            
            elapsed = time.time() - start_time # Calculating how long the measurement itself took
            sleep_time = max(0, interval - elapsed) # Calculating how much time remains to wait to maintain a constant frequency
            
            time.sleep(sleep_time)
        return results
    
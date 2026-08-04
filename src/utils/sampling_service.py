import time
from typing import List
from Ammeters.client import read_current


class SamplingService:
    def __init__(self, ammeter_type: str, samples: int = 10, delay: float = 0.5):
        """
        :param ammeter_type: (greenlee / entes / circutor)
        :param samples: כמה דגימות לקחת
        :param delay: זמן בין דגימות (בשניות)
        """
        self.ammeter_type = ammeter_type
        self.samples = samples
        self.delay = delay

    def read_current_value(self) -> float:
        result = read_current(self.ammeter_type)

        if result is None:
            raise Exception(f"Failed to read from {self.ammeter_type}")

        return result["current"]

    def collect_samples(self) -> List[float]:
        values = []

        for i in range(self.samples):
            try:
                value = self.read_current_value()
                values.append(value)
            except Exception as e:
                print(f"Error reading sample {i}: {e}")

            time.sleep(self.delay)

        return values
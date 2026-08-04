from src.analyzers.measurement_analyzer import MeasurementAnalyzer
from src.utils.sampling_service import SamplingService


class MultiDeviceAnalyzer:
    def __init__(self, ammeter_types, num_samples, interval):
        self.ammeter_types = ammeter_types
        self.num_samples = num_samples
        self.interval = interval

    def analyze(self):
        results = {}
        service = SamplingService()

        for ammeter in self.ammeter_types:
            try:
                measurements = service.read_current_NUM_times(
                    ammeter,
                    self.num_samples,
                    self.interval
                )

                analyzer = MeasurementAnalyzer(measurements)
                summary = analyzer.summary()
                summary["stability"] = analyzer.evaluate_stability(summary)

                results[ammeter] = {
                    "summary": summary,
                    "measurements": measurements
                }

            except Exception as e:
                print(f"Failed analyzing {ammeter}: {e}")

        return results

    def rank_by_stability(self, results):
        return sorted(
            results.items(),
            key=lambda x: x[1]["summary"]["stdev"]
        )

    def print_chart(self, measurements, device_name):
        if not measurements:
            print(f"No data for {device_name}")
            return

        max_val = max(measurements)

        print(f"\n--- Visualization for {device_name} ---")
        for i, val in enumerate(measurements):
            bar = "#" * int((val / max_val) * 50)
            print(f"{i:02d}: {bar} ({round(val, 4)})")

    def visualize_all(self, results):
        for device, data in results.items():
            self.print_chart(data["measurements"], device)
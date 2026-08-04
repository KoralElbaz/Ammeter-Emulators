from src.analyzers.measurement_analyzer import MeasurementAnalyzer
from src.utils.sampling_service import SamplingService


class MultiDeviceAnalyzer:
    def __init__(self, ammeter_types, num_samples, interval):
        self.ammeter_types = ammeter_types
        self.num_samples = num_samples
        self.interval = interval

    def analyze(self):
        results = {}

        for ammeter in self.ammeter_types:
            try:
                # ✅ יוצרים service לכל מכשיר
                service = SamplingService(
                    ammeter_type=ammeter,
                    samples=self.num_samples,
                    delay=self.interval
                )

                # ✅ אוספים דגימות
                measurements = service.collect_samples()

                # ✅ ניתוח
                analyzer = MeasurementAnalyzer(measurements)
                summary = analyzer.summary()

                # ⚠️ לוודא שיש stdev!
                summary["stability"] = analyzer.evaluate_stability(summary)

                summary["measurements"] = measurements

                results[ammeter] = summary

            except Exception as e:
                print(f"Failed analyzing {ammeter}: {e}")

        return results

    def rank_by_stability(self, results):
        return sorted(results.items(), key=lambda x: x[1]["stdev"])

    def visualize_all(self, results):
        from src.visualization.chart_printer import print_chart

        for device, data in results.items():
            print_chart(data["measurements"], device)
from src.analyzers.measurement_analyzer import MeasurementAnalyzer
from src.utils.sampling_service import SamplingService

class MultiDeviceAnalyzer:
    def __init__(self, ammeter_types, num_samples,interval ):
        self.ammeter_types = ammeter_types
        self.num_samples = num_samples
        self.interval = interval

    def analyze(self):
        results = {}
        service = SamplingService()
        for ammeter in self.ammeter_types:
            try:
                measurements = service.read_current_NUM_times(ammeter, self.num_samples,self.interval)
                analyzer = MeasurementAnalyzer(measurements)
                results[ammeter] = analyzer.summary()
            except Exception as e:
                print(f"Failed analyzing {ammeter}: {e}")
        return results

    def rank_by_stability(self, results):
        return sorted(results.items(), key=lambda x: x[1]["stdev"])
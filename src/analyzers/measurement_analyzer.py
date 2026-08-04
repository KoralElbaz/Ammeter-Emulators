class MeasurementAnalyzer:
    def __init__(self, measurements: list):
        self.currents = measurements
        
        if not self.currents:
            raise ValueError("No valid measurements")

    def mean(self):
        return sum(self.currents) / len(self.currents)

    def median(self):
        sorted_vals = sorted(self.currents)
        n = len(sorted_vals)
        mid = n // 2

        if n % 2 == 0:
            return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        return sorted_vals[mid]

    def stdev(self):
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self.currents) / len(self.currents)
        return variance ** 0.5

    def min(self):
        return min(self.currents)

    def max(self):
        return max(self.currents)

    def summary(self):
        if not self.currents:
            raise ValueError("No valid measurements")
    
        return {
            "mean": self.mean(),
            "median": self.median(),
            "stdev": self.stdev(),
            "min": self.min(),
            "max": self.max()
        }
        
    def evaluate_stability(self,summary):
        stdev = summary["stdev"]

        if stdev < 0.05:
            return "Excellent"
        elif stdev < 0.2:
            return "Good"
        elif stdev < 1:
            return "Fair"
        else:
            return "Unstable"
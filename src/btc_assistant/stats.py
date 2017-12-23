import statistics

class MovingAverage:
    def __init__(self, previous_samples, window_size=20):
        self.measurements = previous_samples
        self.window_size = window_size
        self.last_average = statistics.mean(previous_samples)

    def take_measurement(self, numeric_val):
        self.last_average = self.average()
        self.measurements.append(numeric_val)
        if len(self.measurements) > self.window_size:
            self.measurements.pop(0)
    
    def average(self):
        return statistics.mean(self.measurements)
    
    def std_deviation(self):
        return statistics.stdev(self.measurements)
    
    def pct_change(self):
        return 100 * (self.average() / self.last_average - 1)
    
    def upper_quartile(self):
        raise NotImplementedError()
    
    def lower_quartile(self):
        raise NotImplementedError()
    
    def __len__(self):
        return len(self.measurements)
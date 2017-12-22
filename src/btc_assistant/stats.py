import statistics

class StatisticalMeasure:
    def __init__(self, data):
        self.data = data
        
    def average(self, *sample):
        return statistics.mean(*sample)

    def std_deviation(self, *sample):
        return statistics.stdev(*sample)
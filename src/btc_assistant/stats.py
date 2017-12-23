import statistics

class StatisticalMeasure:
    def average(self, *sample):
        return statistics.mean(*sample)

    def std_deviation(self, *sample):
        return statistics.stdev(*sample)
class InMemoryStorage:
    def __init__(self, records=[]):
        self.records = records

    def get_last_records(self, num_records):
        return self.records[-num_records:]

    def store_record(self, record):
        self.records.append(record)
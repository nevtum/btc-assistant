from abc import ABCMeta, abstractmethod

class StorageBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def get_last_records(self, num_records):
        raise NotImplementedError()

class InMemoryStorage(StorageBase):
    def __init__(self, records=[]):
        self.records = records

    def get_last_records(self, num_records):
        return self.records[-num_records:]

    def store_record(self, record):
        self.records.append(record)
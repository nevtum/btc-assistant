from abc import ABCMeta, abstractmethod

class StorageBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def get_last_records(self, num_records):
        raise NotImplementedError()


class FakeStorage(StorageBase):
    def __init__(self):
        self.records = []

    def store_record(self, record):
        self.records.append(record)
    
    def get_last_records(self, num_records):
        raise NotImplementedError("To do!")
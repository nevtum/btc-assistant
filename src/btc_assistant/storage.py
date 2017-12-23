from abc import ABCMeta, abstractmethod

class StorageBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def get_last_records(self, num_records):
        raise NotImplementedError()
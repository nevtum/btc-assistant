import pickle
import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseClass(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_record(self, record):
        raise NotImplementedError()

    @abstractmethod
    def get_last_records(self, num_records):
        raise NotImplementedError()

class PickleStorage(BaseClass):
    def __init__(self, filepath):
        self.pickle_filepath = filepath
    
    def store_record(self, record):
        with open(self.pickle_filepath, "ab") as f:
            logger.info("Pickling record: %s" % record)
            pickle.dump(record, f)
    
    def get_last_records(self, num_records):
        with open(self.pickle_filepath, "rb") as f:
            array = pickle.load(f)
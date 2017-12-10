import pickle
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class PickleStorage:
    def __init__(self, filepath):
        self.pickle_file_handle = open(filepath, "ab")
    
    def store_record(self, record):
        logger.info("Pickling record: %s" % record)
        pickle.dump(record, self.pickle_file_handle)
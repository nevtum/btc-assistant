from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BTCRecord(Base):
    __tablename__ = "btc_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    price = Column(Float)
    volume = Column(Float)
    source = Column(String(100))

    def __repr__(self):
        return "{}(btc_price={})".format(self.__class__.__name__, self.price)

class BTCDomainRecord:
    def __init__(self, db_object):
        self.data = db_object
    
    @property
    def timestamp(self):
        return self.data.timestamp

    @property
    def last_price(self):
        return self.data.price

    @property
    def volume(self):
        return self.data.volume

    def __repr__(self):
        return "{}(id={} btc_price={})".format(
            self.__class__.__name__, self.data.id, self.data.price
        )
    
filename = "btc_data.sqlite"
engine = create_engine("sqlite:///%s" % filename, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_database_storage():
    session = Session()
    return DatabaseStorage(session, "Independent Reserve")
    
class DatabaseStorage:
    def __init__(self, session, data_source):
        self.session = session
        self.data_source = data_source

    def store_record(self, record):
        ds = self.data_source
        obj = BTCRecord(
            timestamp=record.timestamp,
            price=record.last_price,
            volume=record.volume,
            source=self.data_source
        )
        self.session.add(obj)
        self.session.commit()

    def get_last_records(self, num_records):
        db_records = self.session.query(BTCRecord).order_by(BTCRecord.id.desc()).limit(num_records)
        objs = map(lambda r: BTCDomainRecord(r), db_records)
        ordered = reversed(list(objs))
        return list(ordered)
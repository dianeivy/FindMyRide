from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import csv
from sqlalchemy.orm import sessionmaker


def create_findmyride_database(database_name):
    engine = create_engine('postgresql://%s:%s@localhost/%s'%('dianeivy', password, database_name))
    print(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    return engine


Base = declarative_base()
class StationStatus(Base):
    __tablename__ = 'station_statuses'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, index=True)
    event_date = Column(DateTime)
    num_bikes = Column(Integer)
    num_empty_bikes = Column(Integer)
    capacity = Column(Integer)

    def __repr__(self):
        return "<StationStatus(station_id='%d', event_date='%s', num_bikes='%d', num_empty_bikes='%d', capacity='%d')>" \
               %(self.station_id, self.event_date, self.num_bikes, self.num_empty_bikes, self.capacity)


Base2 = declarative_base()
class StationInfo(Base2):
    __tablename__ = 'station_info'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, index=True)
    terminal = Column(String)
    station_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    existing = Column(Boolean)
    num_events = Column(Integer)

    def __repr__(self):
        return "<StationInfo(station_id='%d', terminal='%s', station_name='%s', latitude='%f', longitude='%f', existing='%s', num_events='%d')>" \
               %(self.station_id, self.terminal, self.station_name, self.latitude, self.longitude, self.existing, self.num_events)


def create_station_statuses_table(engine, data_file):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    with open(data_file, 'rb') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        for index, row in enumerate(csv_data):
            if index == 0:
                print row
                continue
            record = StationStatus(**{
                'station_id': int(row[1]),
                'event_date': row[2],
                'num_bikes': int(row[3]),
                'num_empty_bikes': int(row[4]),
                'capacity': int(row[5])
                })
            s.add(record)
            s.commit()
    s.close()

def create_station_info_table(engine, data_file):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    with open(data_file, 'rb') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        for index, row in enumerate(csv_data):
            if index == 0:
                print row
                continue
            if row[5] == 'Existing': exist=True
            else: exist=False
            record = StationInfo(**{
                'station_id': int(row[0]),
                'terminal': row[1],
                'station_name': row[2],
                'latitude': float(row[4]),
                'longitude': float(row[5]),
                'existing': exist,
                'num_events': 0,
                })
            s.add(record)
            s.commit()
    s.close()


def run_db():
    engine = create_findmyride_database('hubway_db4')
    Base.metadata.create_all(engine)
    create_station_statuses_table(engine, '/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/stationstatus/stationstatus4.csv')
    Base2.metadata.create_all(engine)
    create_station_info_table(engine, '/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/hubway_stations.csv')


if __name__ == '__main__':
    run_db()

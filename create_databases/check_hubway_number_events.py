from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
from sqlalchemy.orm import sessionmaker
import glob
from datetime import date, timedelta

db_name = 'hubway_db'


def create_findmyride_database(database_name):
    engine = create_engine('postgresql://%s:%s@localhost/%s'%('dianeivy', password, database_name))
    print(engine.url)
    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    return engine


Base = declarative_base()
class StationCount(Base):
    __tablename__ = 'station_count'

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, index=True)
    event_count = Column(Integer)

    def __repr__(self):
        return "<StationCount(station_id='%d', event_count='%d')>" %(self.station_id, self.event_count)


def count_events(engine):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    con = psycopg2.connect(database=db_name, user='dianeivy', host='localhost', password=password)
    sql_query = "SELECT * FROM station_info;"
    station_info = pd.read_sql_query(sql_query, con)

    sql_query = "SELECT * FROM station_statuses;"
    station_statuses = pd.read_sql_query(sql_query, con)

    for station_id in station_info['station_id'].values:
        record = StationCount(**{'station_id': station_id,
                                 'event_count': station_statuses[(station_statuses['station_id'] == station_id)]['event_date'].count()})


        s.add(record)
        s.commit()
    s.close()


def run_db():
    engine = create_findmyride_database(db_name)
    Base.metadata.create_all(engine)
    count_events(engine)


if __name__ == '__main__':
    run_db()


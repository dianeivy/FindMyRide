from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd


dbname = 'birth_db'
username = 'dianeivy'
pswd = 'password'

## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgresql://%s:%s@localhost/%s'%('dianeivy', 'tmp_password', 'hubway_db'))
print engine.url
# Replace localhost with IP address if accessing a remote server
## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# print 'loading data frame'
# hubway_data = pd.DataFrame.from_csv('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/stationstatus/stationstatus.csv')
#
# print 'in data frame'
# ## insert data into database from Python (proof of concept - this won't be useful for big data, of course)
# ## df is any pandas dataframe
# hubway_data.to_sql('hubway_station_statuses', engine, if_exists='replace')

import csv
con = psycopg2.connect(database='hubway_db', user='dianeivy', host='localhost', password='tmp_password')
with open ('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/stationstatus/stationstatus2.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)
    query = 'insert into MyTable({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    cursor = con.cursor()
    for data in reader:
        cursor.execute(query, data)
    cursor.commit()

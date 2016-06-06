import pandas
from pylab import *

hubway_stations = pandas.read_csv('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/hubway_stations.csv')
station_statuses = pandas.read_csv('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Bikeshare/hubway_2011_07_through_2013_11/stationstatus/stationstatus2.csv')


print station_statuses.info()
print station_statuses.head()

print

station_statuses['update'] = pandas.to_datetime(station_statuses['update'])
station_statuses['day_of_week'] = station_statuses['update'].dt.dayofweek
station_statuses['hour_of_day'] = station_statuses['update'].dt.hour
print set(station_statuses['day_of_week'])
print set(station_statuses['station_id'])


print station_statuses[(station_statuses['station_id']) == 3]['nbBikes']
figure()
plot(station_statuses[(station_statuses['station_id']) == 3]['hour_of_day'], station_statuses[(station_statuses['station_id']) == 3]['nbBikes'], 'ko')
show()
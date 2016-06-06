from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
from pylab import *
from plot_figures import plot_data_parameters
from collections import Counter

con = None
con = psycopg2.connect(database='hubway_db_tmp', user='dianeivy', host='localhost', password='tmp_password')

sql_query = """
SELECT * FROM hubway_station_statuses_tmp WHERE station_id=3;
"""
hubway_station = pd.read_sql_query(sql_query, con)

print hubway_station.head()
print set(hubway_station['station_id'])

hubway_station['update'] = pd.to_datetime(hubway_station['update'])
hubway_station['hour_of_day'] = hubway_station['update'].dt.hour
hubway_station['minute_of_hour'] = hubway_station['update'].dt.minute
hubway_station['day_of_week'] = hubway_station['update'].dt.dayofweek

# print hubway_station['minute_of_hour']

def get_hour(val):
    return val * 60


def get_minute(val):
    return val
    # print val.dt.hour * 2


hubway_station['minute_of_day'] = hubway_station['hour_of_day'].apply(get_hour) + hubway_station['minute_of_hour'].apply(get_minute)



figure()
blah = []
print set(hubway_station['minute_of_day'])
for min in set(hubway_station['minute_of_day']):
    blah.append(hubway_station[(hubway_station['minute_of_day'] == min)]['nbBikes'].mean())
print len(set(hubway_station['minute_of_day']))
print len(blah)
plot(np.arange(1440), np.array(blah))
show()
# plot(np.arange(0, 24 * 60, 1 / 60.), hubway_station['minute_of_day'].mean(), 'k.')
# a = hubway_station['hour_of_day'].apply(get_hour)
# aa=pd.np.array(a)


# blue = np.array([0, 165, 223]) / 255.
# plot_data_parameters(fs_offset=-4)
# fig = figure(facecolor=np.array([34, 34, 34]) / 255., figsize=(4, 3))
# ax = subplot(111)
# for day, day_label, clr in zip(set(hubway_station['day_of_week']),
#                                ['Sunday','Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
#                                ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown']):
#     hour_data = []
#     for hour in set(hubway_station['hour_of_day']):
#         hour_data.append(hubway_station[(hubway_station.day_of_week == day) & (hubway_station.hour_of_day == hour)]['nbBikes'].mean())
#     plot(np.arange(24), np.array(hour_data), clr, lw=3, label=day_label)
# legend(loc='best') #, color='white')
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['left'].set_color(blue)
# ax.spines['bottom'].set_color(blue)
# [tl.set_color(blue) for tl in ax.get_yticklabels()]
# [tl.set_color(blue) for tl in ax.get_xticklabels()]
# xlim(1, 24)
# ylim(0, 20)
# yticks([0, 20])
# xticks([0, 12, 24], ['12am', '12pm', '12am'])
# title('Average number of bikes', color='white', fontweight='bold')
# savefig('bikes.pdf', facecolor=fig.get_facecolor(), transparent=True)
# show()

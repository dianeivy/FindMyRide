import urllib2
import xml.etree.ElementTree as ET
from datetime import datetime
from pylab import *


r = urllib2.Request("http://feeds.thehubway.com/stations/stations.xml") #, headers=hdr)
u = urllib2.urlopen(r)
doc = ET.parse(u)

root=doc.getroot()
print(root.tag)
station_id = []
num_bikes = []
num_empty = []
time_stamp = []
#we now use a for loop to extract the information we are interested in
for country in root.findall('station'):
    if country.find('installed').text == 'true':
        station_id.append(int(country.find('id').text))
        num_bikes.append(int(country.find('nbBikes').text))
        num_empty.append(int(country.find('nbEmptyDocks').text))
        tmp_date = str(country.find('latestUpdateTime').text)[:-3]
        time_stamp.append(datetime.utcfromtimestamp(long(tmp_date)))


figure()
plot(num_bikes, 'k.')
show()

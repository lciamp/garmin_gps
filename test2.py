import time
from lxml import objectify
from datetime import datetime

#namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

#data = open("activity_2612240450.gpx", "r")
#Austin - activity_2506525849.tcx
#Brooklyn - activity_2710384216.tcx
#NYC - activity_2298934172.tcx
file = "./activity_2298934172.tcx"

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
#soup = bs4.BeautifulSoup(data, "lxml")

class GarminParser:

    def __init__(self, file):
        tree = objectify.parse(file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        self.units = 'i'
        self.lat_list = [float(x.text) for x in self.root.xpath('//ns:Position/ns:LatitudeDegrees', namespaces={'ns': namespace})]
        self.lng_list = [float(x.text) for x in self.root.xpath('//ns:Position/ns:LongitudeDegrees', namespaces={'ns': namespace})]
        self.distance_list = [float(x.text) for x in self.root.xpath('.//ns:DistanceMeters', namespaces={'ns': namespace})]
        self.bounds = [min(self.lat_list), min(self.lng_list),max(self.lat_list), max(self.lng_list)]
        self.time_list = [x.text for x in self.root.xpath('//ns:Trackpoint/ns:Time', namespaces={'ns': namespace})]

    def points(self):
        return [{'lat': lat, "lng": lon} for lat, lon in zip(self.lat_list, self.lng_list)]

    def center(self):
        center_lat = (max(self.lat_list) + min(self.lat_list)) / 2
        center_lng = (max(self.lng_list) + min(self.lng_list)) / 2

        return {'lat': center_lat, 'lng': center_lng}

    def distance_total(self):
        if self.units == 'i':
            return round(self.distance_list[-1]/1609.344, 2) if self.distance_list else 0
        else:
            return round(self.distance_list[-1], 2) if self.distance_list else 0

    def total_time(self):
        start_time = self.time_list[0]
        end_time = self.time_list[-1]
        start_time = start_time[11:-5]
        end_time = end_time[11:-5]
        fmt = '%H:%M:%S'


        return datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt)

    @property
    def time_seconds(self):
        start_time = self.time_list[0]
        end_time = self.time_list[-1]
        start_time = start_time[11:-5]
        end_time = end_time[11:-5]
        fmt = '%H:%M:%S'

        delta = datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt)
        return delta.seconds

    
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_mile = self.time_seconds / (self.distance_list[-1] / 1609.344)
        return time.strftime('%M:%S', time.gmtime(secs_per_mile))

    def date(self):
        x = datetime.strftime(self.activity.Id.pyval, '%Y-%m-%dT%H:%M:%SZ')
        #date = x[:-14]
        #time = x[11:-5]
        #fmt = '%b %-d %Y at %H:%M:%S'

        return x.strftime('%Y-%m-%d')
        
#2017-11-05T15:17:32.000Z




myFile = GarminParser(file)
track = myFile.points()

print(myFile.date())



#print(type(myFile.distance_total()))
'''
print('distance: {} miles'.format(myFile.distance_total()))
print('center: {}'.format(myFile.center()))
print('first point: {}'.format(track[0]))
'''
print('total time: {}'.format(myFile.total_time()))


print('pace: {}min/m'.format(myFile.pace()))









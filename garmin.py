from datetime import datetime, timedelta
from lxml import objectify
import time

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

gar = 'files/activity_2710384216.tcx'


class GarminParser:

    def __init__(self, file):

        tree = objectify.parse(file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        self.units = 'i'
        self.lat_list = [float(x.text) for x in
                         self.root.xpath('//ns:Position/ns:LatitudeDegrees', namespaces={'ns': namespace})]
        self.lng_list = [float(x.text) for x in
                         self.root.xpath('//ns:Position/ns:LongitudeDegrees', namespaces={'ns': namespace})]
        self.distance_list = [float(x.text) for x in
                              self.root.xpath('.//ns:DistanceMeters', namespaces={'ns': namespace})]
        self.time_list = [x.text for x in self.root.xpath('//ns:Trackpoint/ns:Time', namespaces={'ns': namespace})]
        self.elevation = [float(x.text) for x in
                         self.root.xpath('//ns:Trackpoint/ns:AltitudeMeters', namespaces={'ns': namespace})]
        self.cleaned_up_time = [i[11:-5] for i in self.time_list]

        self.total_time_seconds = str(timedelta(seconds=len(self.time_list)))

    @property
    def bounds(self):
        return [min(self.lat_list), min(self.lng_list), max(self.lat_list), max(self.lng_list)]

    @property
    def points(self):
        return [{'lat': lat, "lng": lon} for lat, lon in zip(self.lat_list, self.lng_list)]

    @property
    def points_list(self):
        return [list(x) for x in zip(self.lat_list, self.lng_list)]

    @property
    def center(self):
        center_lat = (max(self.lat_list) + min(self.lat_list)) / 2
        center_lng = (max(self.lng_list) + min(self.lng_list)) / 2

        return {'lat': center_lat, 'lng': center_lng}

    @property
    def ele_min_max(self):
        return {'min': min(self.elevation), 'max': max(self.elevation)}

    @property
    def center_list(self):
        center_lat = (max(self.lat_list) + min(self.lat_list)) / 2
        center_lng = (max(self.lng_list) + min(self.lng_list)) / 2

        return [center_lat, center_lng]

    @property
    def distance_total(self):
        if self.units == 'i':
            return round(self.distance_list[-1] / 1609.344, 2) if self.distance_list else 0
        else:
            return round(self.distance_list[-1], 2) if self.distance_list else 0

    @property
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

    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_mile = round(self.time_seconds / (self.distance_list[-1] / 1609.344))
        return time.strftime('%M:%S', time.gmtime(secs_per_mile))


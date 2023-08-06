# coding: utf-8

from __future__ import unicode_literals
import taspy


class Location(object):
    def __init__(self, name, description=None, essids=None, gps_location=None):
        if type(essids) is not list and essids is not None:
            essids = [essids]
        self.name = name
        self.description = description
        self.essids = essids
        self.gps_location = gps_location

    def is_current_location(self):
        return taspy.get_essid() in self.essids

    def __str__(self):
        return 'Location: {}'.format(self.name)

    def __repr__(self):
        return self.__str__()


class UnknownLocation(Location):
    def __str__(self):
        return 'Unknown Location'

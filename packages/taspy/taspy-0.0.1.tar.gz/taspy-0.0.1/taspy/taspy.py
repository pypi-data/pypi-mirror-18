# coding: utf-8

from __future__ import unicode_literals
from wireless import Wireless
import models
import yaml
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_essid():
    logger.debug('Query current essid')
    wireless = Wireless()
    return wireless.current()


class Taspy(object):
    def __init__(self, configfile):
        self.locations = []
        with open(configfile, 'r') as f:
            config = yaml.load(f.read())
            assert 'taspy' in config, 'taspy root element could not be found'
            config = config['taspy']
        for l in config['locations']:
            lname = l.keys()[0]
            essids = l[lname]['essids']
            loc = models.Location(
                name=lname,
                essids=essids
            )
            self.locations.append(loc)
        self.unknown_location = models.UnknownLocation('unknown')

    def __get_location_by_name(self, name):
        for l in self.locations:
            if l.name == name:
                return l

    @property
    def home_location(self):
        return self.__get_location_by_name('home')

    @property
    def work_location(self):
        return self.__get_location_by_name('work')

    @property
    def commute_location(self):
        return self.__get_location_by_name('commute')

    @property
    def at_home(self):
        try:
            return self.home_location.is_current_location()
        except:
            logger.debug('No home location found')
        return False

    @property
    def at_work(self):
        try:
            return self.work_location.is_current_location()
        except:
            logger.debug('No work location found')
        return False

    @property
    def commuting(self):
        try:
            return self.commute_location.is_current_location()
        except:
            logger.debug('No commute location found')
        return False

    @property
    def current_location(self):
        for l in self.locations:
            if l.is_current_location():
                return l
        return self.unknown_location

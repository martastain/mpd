import time

from .constants import *
from .utils import *
from .rfc3339 import timestamptostr as rfc_time

class BaseObject(object):
    keys = []
    defaults = {}

    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        self.attrib = {}
        for key in self.defaults:
            self.attrib[key] = self.defaults[key]
        for key in kwargs:
            if not key in self.keys:
                raise KeyError, "Unexpected key {}".format(key)
            self.attrib[key] = kwargs[key]

    def __getitem__(self, key):
        return self.attrib.get(key, None)

    def __setitem__(self, key, value):
        if not key in self.keys:
            raise KeyError, "Unexpected key {}".format(key)
        self.attrib[key] = value

    def set_time(self, key, value):
        assert type(value) in [int, float]
        self[key] = rfc_time(value)

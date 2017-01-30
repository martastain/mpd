import time

from .common import *
from .objects import *

__all__ = ["MPD"]

class MPD(BaseObject):
    keys = [
            "id",
            "profiles",
            "type",
            "availabilityStartTime",
            "availabilityEndTime",
            "publishTime",
            "mediaPresentationDuration",
            "minimumUpdatePeriod",
            "minBufferTime",
            "timeShiftBufferDepth",
            "suggestedPresentationDelay",
            "maxSegmentDuration",
            "maxSubsegmentDuration"
        ]

    defaults = {
            "xmlns:xsi" : MPD_XMLNS_XSI,
            "xmlns" : MPD_XMLNS,
            "xsi:schemaLocation" : MPD_XSI_LOCATION,
            "profiles" : MPD_PROFILES,
            "profiles" : MPD_PROFILES,
            "type" : "dynamic",
            "availabilityStartTime" : rfc_time(time.time()),
            "publishTime" : rfc_time(time.time()),
            "minimumUpdatePeriod" : "PT10S",
            "minBufferTime" : "PT1S",
            "timeShiftBufferDepth" : "PT10S",
            "maxSegmentDuration" : "PT10S",
            "maxSubsegmentDuration" : "PT10S"
        }

    def __init__(self, **kwargs):
        super(MPD, self).__init__(**kwargs)
        self.periods = []

    def __iter__(self):
        return self.periods.__iter__()

    def add_period(self, **kwargs):
        if not "id" in kwargs:
            kwargs["id"] = len(self.periods)
        if not "start" in kwargs:
            kwargs["start"] = "PT0S"
            #TODO: add start as total duration of previous periods
        self.periods.append(Period(self, **kwargs))
        return self.periods[-1]

    @property
    def xml(self):
        result = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n"
        content = []
        for period in self.periods:
            content.append(period.xml)
        result += mk_xml_tag("MPD", self.attrib, content)
        return result

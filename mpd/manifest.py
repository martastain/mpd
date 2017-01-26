import time

from .common import *
from .objects import *

__all__ = ["MPD"]

class MPD(BaseObject):
    keys = ["id", "profiles", "type", "availabilityStartTime", "availabilityEndTime", "publishTime", "mediaPresentationDuration", "minimumUpdatePeriod", "minBufferTime", "timeShiftBufferDepth", "suggestedPresentationDelay", "maxSegmentDuration", "maxSubsegmentDuration"]

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

    def __getitem__(self, index):
        return self.periods[index]

    def __iter__(self):
        return self.periods.__iter__()

    def add_period(self, **kwargs):
        self.periods.append(Period(**kwargs))
        return self.periods[-1]

    @property
    def xml(self):
        result = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n"
        result += "<MPD {}>\n".format(self.mk_attrs())
        for period in self.periods:
            result += indent(period.xml)
        result += "</MPD>"
        return result




#######################

"""<?xml version="1.0" encoding="utf-8" ?>
<MPD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:mpeg:dash:schema:mpd:2011" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd" type="dynamic" availabilityStartTime="{{NOW}}" timeShiftBufferDepth="PT10S" minimumUpdatePeriod="PT595H" maxSegmentDuration="PT5S" minBufferTime="PT1S" profiles="urn:mpeg:dash:profile:isoff-live:2011,urn:com:dashif:dash264">
    <Period id="1" start="PT0S">

            <AdaptationSet group="1" mimeType="audio/mp4" minBandwidth="128000" maxBandwidth="128000" segmentAlignment="true">
              <Representation id="128kbps" bandwidth="128000" codecs="mp4a.40.2" audioSamplingRate="48000">
                <SegmentTemplate duration="8000" media="test-a-128-$Number$.m4v" initialization="test-a-128-init.mp4" startNumber="{{NUMBER}}" liveEdgeNumber="{{NUMBER}}"/>
              </Representation>
            </AdaptationSet>

            <AdaptationSet group="2" mimeType="video/mp4" segmentAlignment="true">
              <Representation id="4000kbps,1080p" frameRate="25" bandwidth="4000000" codecs="avc1.42c028" width="1920" height="1080">
                <SegmentTemplate duration="8000" media="test-v-4000-$Number$.m4v" initialization="test-v-4000-init.mp4" startNumber="{{NUMBER}}" liveEdgeNumber="{{NUMBER}}"/>
              </Representation>
            </AdaptationSet>

    </Period>
</MPD>"""

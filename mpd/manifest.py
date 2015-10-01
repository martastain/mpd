import os
import time

from .rfc3339 import timestamptostr as rfc_time
from .utils import *
from .constants import *


class SegmentTemplate():
    def __init__(self, **kwargs):
        self.attrs = [
        ]

    @property 
    def xml(self):
        return "<SegmentTemplate {}/>".format(xml_attrs(self.xml_attrs))


class Representation():
    @property
    def xml(self):
        result = "<Representation {}>\n".format(xml_attrs(self.attrs))
        if self.segment_template:
            result += "\n    " + self.segment_template.xml + "\n"    
        result += "</Representation>"
        return result
            

class AdaptationSet():
    def __init__(self, id, **kwargs):
        self.id = id
        self.attrs = [
        ]
        self.segment_template = False
        self.representations = []

    @property
    def xml(self):
        result = "<AdaptationSet {}>\n".format(xml_attrs(self.attrs))
        if self.segment_template:
            result += self.segment_template.xml
        for representation in self.representations:
            result += indent(representation.xml)
        result += "</AdaptationSet>"
        return result


class Period():
    def __init__(self, id, **kwargs):
        self.id = id
        self.attrs = [
            ["id"       : id],
            ["start"    : "PT0S"]
        ]
        self.adaptation_sets = []

    @property
    def xml(self):
        result = "<Period {}>\n".format(xml_attrs(self.attrs))
        for adaptation_set in self.adaptation_sets:
            result += indent(adaptation_set.xml)
        result += "</Period>"
        return result


class MPD():
    def __init__(self, **kwargs):
        self.start_time = kwargs.get("start_time", False) or time.time()
        
        # I'm sorry for PEP-8 violation here. I need readability here...
        self.attrs = [
            ["xmlns:xsi",                   MPD_XMLNS_XSI],
            ["xmlns",                       MPD_XMLNS],
            ["xsi:schemaLocation",          MPD_XSI_LOCATION],
            ["profiles",                    MPD_PROFILES],
            ["id",                          kwargs.get("id", None)],
            ["type",                        kwargs.get("type", "dynamic")],
            ["availabilityStartTime",       kwargs.get("availabilityStartTime", self.start_time)],
            ["availabilityEndTime",         kwargs.get("availabilityEndTime", None)],
            ["publishTime",                 kwargs.get("publishTime", self.start_time)],
            ["mediaPresentationDuration",   kwargs.get("mediaPresentationDuration", None)],
            ["minimumUpdatePeriod",         kwargs.get("minimumUpdatePeriod", "PT10S")],
            ["minBufferTime",               kwargs.get("minBufferTime", "PT1S")],
            ["timeShiftBufferDepth",        kwargs.get("timeShiftBufferDepth", "PT10S")],
            ["suggestedPresentationDelay",  kwargs.get("suggestedPresentationDelay", None)],
            ["maxSegmentDuration",          kwargs.get("maxSegmentDuration", "PT10S")],
            ["maxSubsegmentDuration",       kwargs.get("maxSubsegmentDuration", "PT10S")]
        ]
        self.periods = []

    def __getitem__(self, index):
        return self.periods[index]

    def __iter__(self):
        return self.periods.__iter__()

    def add_period(self, **kwargs):
        id_period = len(self.periods) + 1      # This is probably stupid
        period = Period(id_period, **kwargs)
        self.periods.append(period)
        return self.periods[-1]

    def mk_attrs(self):
        return xml_attrs(self.attrs)

    @property
    def xml(self):
        result = "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n"
        result += "<MPD {}>\n".format(self.mk_attrs())
        for period in self.periods:
            result += indent(period.xml)
        result += "</MPD>"
        return result




#######################
## This is ugly



    @property
    def manifest(self):
        body = ""

        for adaptation_set in self.asset.adaptation_sets:

            if adaptation_set.id != "v":
                continue

            body += indent(4, "<AdaptationSet {}>".format(adaptation_set.xmlmeta ))
            for representation in adaptation_set.representations:

                if representation.id not in ["v-4000", "a-128"]:
                    continue

                timescale = int(representation.template.get("timescale", 1))

                tpl_params = {
                    "media"            : "{}-{}-$Number${}".format(self.key, representation.id, os.path.splitext(representation.template["media"])[1]),
                    "initialization"   : "{}-{}-init{}".format(self.key, representation.id, os.path.splitext(representation.template["initialization"])[1]),
                    "timescale"        : timescale,
                    "duration"         : int(self.asset.segment_duration),
                    "start_number"     : self.start_number,
                    "live_edge_number" : self.start_number
                }

                body += indent(8,  "<Representation {}>".format(representation.xmlmeta))
#                body += indent(12, "<SegmentTemplate {}/>".format(representation.xmltplmeta))
                body += indent(12, "<SegmentTemplate timescale=\"{timescale}\" duration=\"{duration}\" media=\"{media}\" initialization=\"{initialization}\" startNumber=\"{start_number}\" liveEdgeNumber=\"{live_edge_number}\"/>".format(**tpl_params))
                body += indent(8,  "</Representation>")
            body += indent(4, "</AdaptationSet>\n")


        return """<?xml version="1.0" encoding="utf-8" ?>
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
</MPD>""".replace("{{NUMBER}}", str(self.start_number)).replace("{{NOW}}", rfc3339.timestamptostr(self.now))

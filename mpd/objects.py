from .common import *

__all__ = ["SegmentTemplate", "Representation", "AdaptationSet", "Period"]


class SegmentTemplate(BaseObject):
    keys = [
            "media",
            "index",
            "initialization",
            "bitstreamSwitching"
        ] + MULTIPLE_SEGMENT_BASE_TYPE_KEYS

    @property
    def xml(self):
        return "<SegmentTemplate {}/>".format(mk_xml_attrs(self.attrib))


class Representation(BaseObject):
    keys = [
            "id",
            "bandwidth",
            "qualityRanking",
            "dependencyId",
            "mediaStreamStructureId"
        ] + REPRESENTATION_BASE_TYPE_KEYS

    def __init__(self, parent, **kwargs):
        super(Representation, self).__init__(parent, **kwargs)
        self.segment_template = None

    @property
    def xml(self):
        content = []
        if self.segment_template:
            content = [self.segment_template.xml]
        return mk_xml_tag("Representation", self.attrib, content)


class AdaptationSet(BaseObject):
    keys = [
            "id",
            "group",
            "lang",
            "contentType",
            "par",
            "minBandwidth",
            "maxBandwidth",
            "minWidth",
            "maxWidth",
            "minHeight",
            "maxHeight",
            "minFrameRate",
            "maxFrameRate",
            "segmentAlignment",
            "subsegmentAlignment",
            "subsegmentStartsWithSAP",
            "bitstreamSwitching",
        ] + REPRESENTATION_BASE_TYPE_KEYS

    defaults = {}

    def __init__(self, parent, **kwargs):
        super(AdaptationSet, self).__init__(parent, **kwargs)
        self.segment_template = None
        self.representations = []

    @property
    def xml(self):
        content = []
        if self.segment_template:
            content.append(self.segment_template.xml)
        for representation in self.representations:
            content.append(representation.xml)
        return mk_xml_tag("AdaptationSet", self.attrib, content)

    def add_representation(self, **kwargs):
        if not "id" in kwargs:
            kwargs["id"] = len(self.adaptation_sets)
        self.representations.append(Representation(self, **kwargs))
        return self.representations[-1]


class Period(BaseObject):
    keys = ["id", "start"]

    def __init__(self, parent, **kwargs):
        super(Period, self).__init__(parent, **kwargs)
        self.adaptation_sets = []

    @property
    def xml(self):
        return mk_xml_tag("Period", self.attrib, [c.xml for c in self.adaptation_sets])

    def add_adaptation_set(self, **kwargs):
        if not "id" in kwargs:
            kwargs["id"] = len(self.adaptation_sets)
        self.adaptation_sets.append(AdaptationSet(self, **kwargs))
        return self.adaptation_sets[-1]


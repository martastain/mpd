from .common import *

__all__ = ["SegmentTemplate", "Representation", "AdaptationSet", "Period"]



class SegmentTemplate(BaseObject):
    keys = ["media", "index", "initialization", "bitstreamSwitching", "duration", "startNumber"]

    @property
    def xml(self):
        return "<SegmentTemplate {}/>".format(xml_attrs(self.attrs))


class Representation(BaseObject):
    def __init__(self, parent, **kwargs):
        super(Representation, self).__init__(parent, **kwargs)
        self.segment_template = None

    @property
    def xml(self):
        result = "<Representation {}>\n".format(xml_attrs(self.attrs))
        if self.segment_template:
            result += "\n    " + self.segment_template.xml + "\n"
        result += "</Representation>"
        return result


class AdaptationSet(BaseObject):
    keys = []
    defaults = {}

    def __init__(self, parent, **kwargs):
        super(AdaptationSet, self).__init__(parent, **kwargs)
        self.segment_template = None
        self.representations = []

    @property
    def xml(self):
        result = "<AdaptationSet {}>\n".format(xml_attrs(self.attrs))
        if self.segment_template:
            result += indent(self.segment_template.xml)
        for representation in self.representations:
            result += indent(representation.xml)
        result += "</AdaptationSet>"
        return result


class Period(BaseObject):
    keys = ["id", "start"]

    def __init__(self, parent, **kwargs):
        super(Period, self).__init__(parent, **kwargs)
        self.attrs = [
            ["id",       id],
            ["start",    "PT0S"]
        ]
        self.adaptation_sets = []

    @property
    def xml(self):
        result = "<Period {}>\n".format(xml_attrs(self.attrs))
        for adaptation_set in self.adaptation_sets:
            result += indent(adaptation_set.xml)
        result += "</Period>"
        return result



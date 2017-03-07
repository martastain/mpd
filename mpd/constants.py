MPD_XMLNS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
MPD_XMLNS = "urn:mpeg:dash:schema:mpd:2011"
MPD_XSI_LOCATION = "urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd"
MPD_PROFILES = "urn:mpeg:dash:profile:isoff-live:2011"


SEGMENT_BASE_TYPE_KEYS = [
        "timescale",
        "presentationTimeOffset",
        "indexRange",
        "indexRangeExact",
        "availabilityTimeOffset",
        "availabilityTimeComplete",
]

MULTIPLE_SEGMENT_BASE_TYPE_KEYS = [
        "duration",
        "startNumber"
    ] + SEGMENT_BASE_TYPE_KEYS

REPRESENTATION_BASE_TYPE_KEYS = [
        "profiles",
        "width",
        "height",
        "sar",
        "frameRate",
        "audioSamplingRate",
        "mimeType",
        "segmentProfiles",
        "codecs",
        "maximumSAPPeriod",
        "startWithSAP",
        "maxPlayoutRate",
        "codingDependency" ,
        "scanType"
    ]



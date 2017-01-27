def indent(src, l=4):
    return "\n".join(["{}{}\n".format(l*" ", s) for s in src.strip().split("\n")])

def xml_attrs(attrs):
    return " ".join(["{}=\"{}\"".format(key, attrs[key]) for key in attrs if attrs[key] is not None])

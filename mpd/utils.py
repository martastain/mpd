def indent(src, l=4):
    return "\n".join(["{}{}\n".format(l*" ", s) for s in src.split("\n")])


def xml_attrs(attrs):
    return " ".join(["{}=\"{}\"".format(*attr) for attr in attrs if attr[1] is not None])
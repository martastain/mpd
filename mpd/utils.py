__all__ = ["indent", "mk_xml_attrs", "mk_xml_tag"]


def indent(src, l=4):
    result = ""
    for line in src.split("\n"):
       result += l * " "
       result += line
       result += "\n"
    return result

def attr_format(val):
    if val is True:
        return "true"
    elif val is False:
        return "false"
    return val


def mk_xml_attrs(attrs):
    return " ".join(["{}=\"{}\"".format(key, attr_format(attrs[key])) for key in attrs if attrs[key] is not None])


def mk_xml_tag(name, attrs, contents=[]):
    result = "<{}".format(name)
    if attrs:
        result += " " + mk_xml_attrs(attrs)
    if not contents:
        result += "/>"
    else:
        result += ">\n"
        result += indent("\n".join(contents) )
        result += "</{}>".format(name)
    return result

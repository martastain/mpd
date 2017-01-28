def indent(src, l=4):
    result = ""
    for line in src.split("\n"):
       result += l * " "
       result += line
       result += "\n"
    return result


def xml_attrs(attrs):
    return " ".join(["{}=\"{}\"".format(key, attrs[key]) for key in attrs if attrs[key] is not None])


def mk_tag(name, attrs, contents=[]):
    result = "<{}".format(name)
    if attrs:
        result += " " + xml_attrs(attrs)
    if not contents:
        result += "/>"
    else:
        result += ">\n"
        result += indent("\n".join(contents) )
        result += "</{}>".format(name)
    return result

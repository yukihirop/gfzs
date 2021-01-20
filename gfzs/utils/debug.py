import pprint

pp = pprint.PrettyPrinter(indent=2)


def log(name, s=""):
    with open("./tmp/gfzs.log", "a") as f:
        f.write(str(name) + ":" + str(s) + "\n")


def dump(obj):
    with open("./tmp/gfzs.log", "a") as f:
        f.write(pp.pformat(obj) + "\n")

    return obj

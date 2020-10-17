import getopt
import sys
import os

##
# Gets the command line options. Currently:
# -d : int
def get_opts():
    argv = sys.argv[1:]
    opts = dict(getopt.getopt(argv, "d:")[0])
    d = int(opts["-d"]) if "-d" in opts else 1
    return {"d": d}

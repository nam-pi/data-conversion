import datetime
import getopt
import sys
from os import getcwd, path


class Env:
    argv = sys.argv[1:]
    opts = dict(getopt.getopt(argv, "d:p:g:o:f:l:n:")[0])
    cache_validity_days = int(opts["-d"]) if "-d" in opts else 1
    cache_path = opts["-p"] if "-p" in opts else path.join(
        getcwd(), "cache/csv")
    google_cred_path = (
        opts["-g"] if "-g" in opts else path.join(
            getcwd(), ".credentials.json")
    )
    out_path = opts["-o"] if "-o" in opts else path.join(
        getcwd(), "out", "nampi_data_" + str(datetime.datetime.now().timestamp()) + ".ttl")
    out_format = opts["-f"] if "-f" in opts else "turtle"
    log_file = opts["-l"] if "-l" in opts else "conversion.log"
    data_namespace_prefix = opts["-n"] if "-n" in opts else "http://localhost:4000"

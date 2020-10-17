from modules.tables import Tables, Col_heading
import modules.utils as utils
import getopt
import sys
import os

"""
Command line args are:
    -d: -1, 0, or any other positive int
        The number of days the cache files are valid.
            -1: Files valid indefinitely
            0: Files invalid
            other number: the number of days a file is valid
"""

opts = utils.get_opts()

tables = Tables(
    cache_path=os.path.join(os.getcwd(), "cache/csv"),
    credentials_path=os.path.join(os.getcwd(), ".credentials.json"),
    cache_validity_days=opts["d"],
)

print(tables.births)

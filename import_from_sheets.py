from modules.tables import Tables, Col_heading
from modules.rdf_namespaces import Namespace
from modules.nampi_graph import Nampi_graph
import modules.utils as utils
import getopt
import sys
import os
from modules.person import Person
from modules.date import Date

"""
Command line args are:
    -d: -1, 0, or any other positive int
        The number of days the cache files are valid.
            -1: Files valid indefinitely
            0: Files invalid
            other number: the number of days a file is valid
"""

CACHE_PATH = os.path.join(os.getcwd(), "cache/csv")
CREDENTIALS_PATH = os.path.join(os.getcwd(), ".credentials.json")
OUT_PATH = os.path.join(os.getcwd(), "out", "nampi_data.ttl")
OUT_FORMAT = "turtle"

opts = utils.get_opts()

tables = Tables(
    CACHE_PATH,
    CREDENTIALS_PATH,
    cache_validity_days=opts["d"],
)

graph = Nampi_graph()

# Births
for index, row in tables.births.iterrows():
    date = Date.optional(
        graph,
        tables,
        row[Col_heading.exact_date],
        row[Col_heading.earliest_date],
        row[Col_heading.latest_date],
    )
    person = Person(graph, tables, row[Col_heading.person])


file = open(OUT_PATH, "w")
file.write(graph.serialize(OUT_FORMAT))
file.close()

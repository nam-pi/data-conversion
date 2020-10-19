"""Conversion script that transforms data from the temporary NAMPI input table on Google Sheets to RDF.

Command-Line Parameters:
    d (number): The number of days cached files are valid. In addition to positive numbers, "-1" means 
                a file is only refetched if it is currently missing, "0" means they are always refetched.
                Defaults to "1"
    f (str): The path for the cache files. Defaults to 'cache/csv' inside the script root folder.
    c (str): The path to the credentials JSON file. Defaults to ".credentials.json" inside the script root folder.
    o (str): The output file path. Defaults to "out/nampi_data.ttl" inside the script root folder.
    r (str): The rdf file output format. Defaults to "turtle". Can by any of the available formats from "rdflib".

Paths:
    By default, the cache and output paths are located in the script root directory
"""
import errno
import getopt
import os
import sys
from os import getcwd, path, remove

from modules.nampi_data_entry_form_parser import Nampi_data_entry_form_parser
from modules.nampi_graph import Nampi_graph

"""Read command line arguments"""
argv = sys.argv[1:]
opts = dict(getopt.getopt(argv, "d:p:c:o:f:")[0])
cache_validity_days = int(opts["-d"]) if "-d" in opts else 1
cache_path = opts["-p"] if "-p" in opts else path.join(getcwd(), "cache/csv")
cred_path = opts["-c"] if "-c" in opts else path.join(getcwd(), ".credentials.json")
out_path = opts["-o"] if "-o" in opts else path.join(getcwd(), "out", "nampi_data.ttl")
out_format = opts["-f"] if "-f" in opts else "turtle"

print()
print("************************************")
print("* NAMPI data transformation script *")
print("*                                  *")
print("************************************")

"""Create the data graph"""
nampi_graph = Nampi_graph()

"""Parse data to RDF"""
Nampi_data_entry_form_parser(nampi_graph, cache_path, cred_path, cache_validity_days)

"""Write RDF graph to file"""
print("\nSerialize graph")
try:
    os.makedirs(os.path.split(out_path)[0])
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
if path.isfile(out_path):
    remove(out_path)
    print("\tOld output file removed at '{}'".format(out_path))
file = open(out_path, "w")
file.write(nampi_graph.graph.serialize(format=out_format).decode("utf-8"))
print("\tNew output file written at '{}'".format(out_path))
file.close()

print("\n\nFinished successfully")

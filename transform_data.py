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
import getopt
import os
import sys
from os import getcwd, path, remove

from modules.parser import Parser
from modules.tables import Column, Tables

"""Read command line arguments"""
argv = sys.argv[1:]
opts = dict(getopt.getopt(argv, "d:p:c:o:f:")[0])
cache_validity_days = int(opts["-d"]) if "-d" in opts else 1
cache_path = opts["-p"] if "-p" in opts else path.join(getcwd(), "cache/csv")
cred_path = opts["-c"] if "-c" in opts else path.join(getcwd(), ".credentials.json")
out_path = opts["-o"] if "-o" in opts else path.join(getcwd(), "out", "nampi_data.ttl")
out_format = opts["-f"] if "-f" in opts else "turtle"

"""Parse data to RDF"""
tables = Tables(cache_path, cred_path, cache_validity_days)
graph = Parser(tables).parse()

"""Write RDF graph to file"""
if path.isfile(out_path):
    remove(out_path)
    print("Old output file removed")
file = open(out_path, "w")
file.write(graph.serialize(format=out_format).decode("utf-8"))
print("New output file written")
file.close()

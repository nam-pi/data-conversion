"""Conversion script that transforms data from the temporary NAMPI input table on Google Sheets to RDF.

Command-Line Parameters:
    d (number): The number of days cached files are valid. In addition to positive numbers, "-1" means 
                a file is only refetched if it is currently missing, "0" means they are always refetched.
                Defaults to "1"
    f (str): The path for the cache files. Defaults to 'cache/csv' inside the script root folder.
    c (str): The path to the credentials JSON file. Defaults to ".credentials.json" inside the script root folder.
    o (str): The output file path. Defaults to "out/nampi_data.ttl" inside the script root folder.
    r (str): The rdf file output format. Defaults to "turtle". Can by any of the available formats from "rdflib".
    l (str): The path to the logfile. defaults to "conversion.log"

Paths:
    By default, the cache and output paths are located in the script root directory
"""
import datetime
import errno
import getopt
import logging
import os
import sys
from os import getcwd, path, remove

from modules.nampi_graph import Nampi_graph
from parsers.nampi_data_entry_form.nampi_data_entry_form_parser import \
    Nampi_data_entry_form_parser

"""Read command line arguments"""
argv = sys.argv[1:]
opts = dict(getopt.getopt(argv, "d:p:g:o:f:l:")[0])
cache_validity_days = int(opts["-d"]) if "-d" in opts else 1
cache_path = opts["-p"] if "-p" in opts else path.join(getcwd(), "cache/csv")
google_cred_path = (
    opts["-g"] if "-g" in opts else path.join(getcwd(), ".credentials.json")
)
out_path = opts["-o"] if "-o" in opts else path.join(
    getcwd(), "out", "nampi_data_" + datetime.datetime.now().isoformat() + ".ttl")
out_format = opts["-f"] if "-f" in opts else "turtle"
log_file = opts["-l"] if "-l" in opts else "conversion.log"


""" Init logging """
if path.isfile(log_file):
    remove(log_file)
logging.basicConfig(
    filename=log_file,
    format="%(asctime)s,%(msecs)d %(filename)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


logging.info("************************************")
logging.info("* NAMPI data conversion script     *")
logging.info("*                                  *")
logging.info("************************************")

"""Create the data graph"""
nampi_graph = Nampi_graph()

"""Parse the various data sources to RDF"""
Nampi_data_entry_form_parser(
    nampi_graph, cache_path, google_cred_path, cache_validity_days
)

"""Write RDF graph to file"""
logging.info("Serialize graph")
try:
    os.makedirs(os.path.split(out_path)[0])
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
if path.isfile(out_path):
    remove(out_path)
    logging.info("Old output file removed at '{}'".format(out_path))
file = open(out_path, "w")
file.write(nampi_graph.graph.serialize(format=out_format).decode("utf-8"))
logging.info("New output file written at '{}'".format(out_path))
file.close()

logging.info("Finished successfully")

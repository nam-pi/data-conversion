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
import errno
import logging
import os
from os import path, remove

from modules.cli_param import Env
from modules.nampi_graph import Nampi_graph
from parsers.nampi_data_entry_form.nampi_data_entry_form_parser import \
    Nampi_data_entry_form_parser

""" Init logging """
if path.isfile(Env.log_file):
    remove(Env.log_file)
logging.basicConfig(
    filename=Env.log_file,
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
    nampi_graph, Env.cache_path, Env.google_cred_path, Env.cache_validity_days
)

"""Write RDF graph to file"""
logging.info("Serialize graph")
try:
    os.makedirs(os.path.split(Env.out_path)[0])
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
if path.isfile(Env.out_path):
    remove(Env.out_path)
    logging.info("Old output file removed at '{}'".format(Env.out_path))
file = open(Env.out_path, "w")
file.write(nampi_graph.graph.serialize(format=Env.out_format).decode("utf-8"))
logging.info("New output file written at '{}'".format(Env.out_path))
file.close()

logging.info("Finished successfully")

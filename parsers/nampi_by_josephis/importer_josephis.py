# -*- coding: utf-8 -*-
from lxml import etree
import logging
import glob
import sys
import os
import requests
from requests.api import get
import xmltodict
import json
from types import SimpleNamespace
from collections import OrderedDict
from modules.nampi_graph import Nampi_graph
from parsers.nampi_by_josephis.nampi_data_entry_form_josephis import Nampi_data_entry_form_parser_josephis

# prepare dicts
ns = dict(
    aodl="http://pdr.bbaw.de/namespaces/aodl/",
    exist="http://exist.sourceforge.net/NS/exist",
    mods="http://www.loc.gov/mods/v3",
    podl="http://pdr.bbaw.de/namespaces/podl/",
)




class Importer_Josephis:
    _graph: Nampi_graph

    def __init__(self, graph: Nampi_graph):
        self._graph = graph
        josephis_parser = Nampi_data_entry_form_parser_josephis(self._graph)
        print("--Starte Josephis-Daten Erstellung--")
        
        josephis_parser.createJosephis()

        print("--Beende Josephis-Daten Erstellung--")
        

    
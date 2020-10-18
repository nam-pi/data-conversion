"""The module for the Parser class.

Classes:
    Parser

"""

from modules.date import Date
from modules.nampi_graph import Nampi_graph
from modules.person import Person
from modules.place import Place
from modules.source import Source
from modules.source_location import Source_location
from modules.tables import Column, Table, Tables
from rdflib import Graph


class Parser:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    __tables: Tables
    __graph: Nampi_graph

    def __init__(self, tables: Tables):
        """Initialize the class.

        Parameters:
            tables (Tables): The data tables.
        """
        self.__tables = tables
        self.__graph = Nampi_graph()

    def parse(self) -> Graph:
        """Parse the input data and return the resulting RDF graph.

        Returns:
            Graph: the tabular data as RDF.
        """
        self.__parse_births()
        return self.__graph.graph

    def __parse_births(self):
        for _, row in self.__tables.get_table(Table.BIRTHS).iterrows():
            date = Date.optional(
                self.__graph,
                self.__tables,
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            person = Person(
                self.__graph,
                self.__tables,
                row[Column.person],
            )
            place = Place.optional(
                self.__graph,
                self.__tables,
                row[Column.event_place],
            )
            source = Source(self.__graph, self.__tables, row[Column.source])
            source_location = Source_location(
                self.__graph, self.__tables, source, row[Column.source_location]
            )

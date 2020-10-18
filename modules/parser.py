"""The module for the Parser class.

Classes:
    Parser
"""

from modules.birth import Birth
from modules.death import Death
from modules.di_act import Di_act
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.tables import Table, Tables
from pandas import Series
from rdflib import Graph


class Parser:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    _tables: Tables
    _graph: Nampi_graph

    def __init__(self, tables: Tables):
        """Initialize the class.

        Parameters:
            tables (Tables): The data tables.
        """
        self._tables = tables
        self._graph = Nampi_graph()

    def parse(self) -> Graph:
        """Parse the input data and return the resulting RDF graph.

        Returns:
            Graph: the tabular data as RDF.
        """
        self.__add_births()
        self.__add_deaths()
        return self._graph.graph

    def __add_births(self):
        for _, row in self._tables.get_table(Table.BIRTHS).iterrows():
            birth = Birth(self._graph, self._tables, row)
        self.__add_di_act(row, birth)

    def __add_deaths(self):
        for _, row in self._tables.get_table(Table.DEATHS).iterrows():
            death = Death(self._graph, self._tables, row)
        self.__add_di_act(row, death)

    def __add_di_act(self, row: Series, event: Event):
        Di_act(self._graph, self._tables, event, row)

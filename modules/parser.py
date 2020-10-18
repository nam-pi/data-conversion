"""The module for the Parser class.

Classes:
    Parser
"""

from modules.date import Date
from modules.di_act import Di_act
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place
from modules.tables import Column, Table, Tables
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
        self.__parse_births()
        return self._graph.graph

    def __parse_births(self):
        for _, row in self._tables.get_table(Table.BIRTHS).iterrows():
            date = Date.optional(
                self._graph,
                self._tables,
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            person = Person(
                self._graph,
                self._tables,
                row[Column.person],
            )
            place = Place.optional(
                self._graph,
                self._tables,
                row[Column.event_place],
            )
            event = Event(
                self._graph, self._tables, Nampi_type.Core.birth, "", date, place
            )
            event.add_relationship(Nampi_type.Core.starts_life_of, person)
            di_act = Di_act(
                self._graph,
                self._tables,
                event,
                row[Column.author],
                row[Column.source],
                row[Column.source_location],
                row[Column.interpretation_date],
                row[Column.comment],
            )

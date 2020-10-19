"""The module for the Di_act class.

Classes:
    Di_act
"""
import datetime
from typing import Optional

from modules.date import Date
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.resource import Resource
from modules.source_location import Source_location
from modules.tables import Column, Tables
from pandas import Series
from rdflib import RDFS


class Di_act(Resource):
    """An document interpretation act RDF resource."""

    def __init__(
        self, graph: Nampi_graph, tables: Tables, event: Event, row: Series
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            event: The event of the document interpretation act.
            row: The data row for the document interpretation act.
        """
        super().__init__(
            graph,
            tables,
            Nampi_type.Core.document_interpretation_act,
            Nampi_ns.acts,
        )
        date = Date(
            graph,
            tables,
            row[Column.interpretation_date]
            if row[Column.interpretation_date]
            else datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        source_location = Source_location(
            self._graph,
            self._tables,
            row[Column.source],
            row[Column.source_location],
        )
        author = Person(graph, tables, row[Column.author])
        self.add_relationship(Nampi_type.Core.has_interpretation, event)
        self.add_relationship(Nampi_type.Core.is_authored_by, author)
        self.add_relationship(Nampi_type.Core.has_source_location, source_location)
        self.add_relationship(Nampi_type.Core.is_authored_on, date)
        if row[Column.comment]:
            self.add_relationship(
                RDFS.comment, Nampi_graph.string_literal(row[Column.comment])
            )

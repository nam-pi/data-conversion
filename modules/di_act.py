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
from modules.tables import Tables
from rdflib import RDFS


class Di_act(Resource):
    """An document interpretation act RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        event: Event,
        author_label: str,
        source_label: str,
        source_location_text: str,
        interpretation_date: Optional[str],
        comment: Optional[str],
    ):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the person belongs to.
            tables (Tables): The data tables.
            event: The event of the document interpretation act.
            author_label (str): The label of the author of the document interpretation act.
            source_label (str)
            source_location_text (str): The source location of the document interpretation act.
            interpretation_date (Optional[str]): The interpretation date as a string of the format "YYYY-MM-DD". If it is missing, the current date is used.
            comment (str): An optional comment.
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
            interpretation_date
            if interpretation_date
            else datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        source_location = Source_location(
            self._graph,
            self._tables,
            source_label,
            source_location_text,
        )
        author = Person(graph, tables, author_label)
        self.add_relationship(Nampi_type.Core.has_interpretation, event)
        self.add_relationship(Nampi_type.Core.is_authored_by, author)
        self.add_relationship(Nampi_type.Core.has_source_location, source_location)
        self.add_relationship(Nampi_type.Core.is_authored_on, date)
        if comment:
            self.add_relationship(RDFS.comment, Nampi_graph.string_literal(comment))

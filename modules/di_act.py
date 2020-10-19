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
from rdflib import RDFS


class Di_act(Resource):
    """An document interpretation act RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        event: Event,
        author: Person,
        source_location: Source_location,
        interpretation_date_text: Optional[str],
        comment_text: Optional[str],
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            event: The event of the document interpretation act.
            author: The author of the document interpretation act.
            source_location: The location the interpretation was made.
            interpretation_date_text: The text of the interpretation date in the form "YYYY-MM-DD".
            comment_text: The event comment.

        """
        super().__init__(
            graph,
            Nampi_type.Core.document_interpretation_act,
            Nampi_ns.acts,
        )
        date = Date(
            graph,
            interpretation_date_text
            if interpretation_date_text
            else datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        self.add_relationship(Nampi_type.Core.has_interpretation, event)
        self.add_relationship(Nampi_type.Core.is_authored_by, author)
        self.add_relationship(Nampi_type.Core.has_source_location, source_location)
        self.add_relationship(Nampi_type.Core.is_authored_on, date)
        if comment_text:
            self.add_relationship(
                RDFS.comment, Nampi_graph.string_literal(comment_text)
            )

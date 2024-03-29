"""The module for the Di_act class.

Classes:
    Di_act
"""
import datetime
from typing import Optional

from rdflib import RDFS

from modules.author import Author
from modules.date import Date
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource
from modules.source_location import Source_location


class Di_act(Resource):
    """An document interpretation act RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        event: Event,
        authors,
        source_location: Source_location,
        interpretation_date_text: Optional[str],
        comment_text: Optional[str] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            event: The event of the document interpretation act.
            authors: List of authors of the document interpretation act.
            source_location: The location the interpretation was made.
            interpretation_date_text: The text of the interpretation date in the form "YYYY-MM-DD".
            comment_text: The event comment.

        """
        super().__init__(graph, Nampi_type.Core.act,
                         Nampi_ns.act, "Document interpretation act", True)
        date = Date(graph, interpretation_date_text if interpretation_date_text else datetime.datetime.now(
        ).strftime("%Y-%m-%d"))
        self.add_relationship(Nampi_type.Core.has_interpretation, event)

        if type(authors) is not Author:
            if len(authors) == 1:
                author = Author(self._graph, authors)
                self.add_relationship(Nampi_type.Core.is_authored_by, author)
            else:
                for authoritem in authors:
                    author = Author(self._graph, authoritem)
                    self.add_relationship(Nampi_type.Core.is_authored_by, author)
        else: 
            self.add_relationship(Nampi_type.Core.is_authored_by, authors)
        self.add_relationship(
            Nampi_type.Core.has_source_location, source_location)
        self.add_relationship(Nampi_type.Core.is_authored_on, date)
        if comment_text:
            self.add_relationship(
                RDFS.comment, Nampi_graph.string_literal(comment_text)
            )

"""The module for the Title class.

Classes:
    Group
"""
from __future__ import annotations

from rdflib import URIRef

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Title(Resource):
    """A group RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        text: str,
        title_type: URIRef = Nampi_type.Core.title,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the title belongs to.
            text: The text for the title.
            title_type: The optional URI of the title type.
        """
        label = "Title"
        if title_type == Nampi_type.Mona.religious_title:
            label = "Religious title"
        super().__init__(graph, title_type, Nampi_ns.aspect, label, True)
        self.add_relationship(obj=self._graph.string_literal(
            text), pred=Nampi_type.Core.has_xsd_string)

"""The module for the Source_location class.

Classes:
    Source_location
"""
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.source import Source


class Source_location(Node):
    """A blank node with associated triples that represents a location in a source."""

    def __init__(self, graph: Nampi_graph, source: Source, location: str):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the source location belongs to.
            source: The source the location belongs to.
            location: The location string (page name, url or similar).
        """
        super().__init__(graph, Nampi_type.Core.source_location)
        self.add_relationship(Nampi_type.Core.has_source, source)
        self.add_relationship(
            Nampi_type.Core.has_xsd_string,
            Nampi_graph.string_literal(location),
        )

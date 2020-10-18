"""The module for the Source_location class.

Classes:
    Source_location

"""
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.source import Source
from modules.tables import Tables


class Source_location(Node):
    """A blank node with associated triples that represents a location in a source."""

    def __init__(
        self, graph: Nampi_graph, tables: Tables, source: Source, location: str
    ):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the source location belongs to.
            tables (Tables): The data tables.
            source (Source): The source the source locatino belongs to.
            location (str): The location string (page name, url or similar).
        """
        super().__init__(graph, tables, Nampi_type.Core.source_location)
        self.add_relationship(Nampi_type.Core.has_source, source.node)
        self.add_relationship(
            Nampi_type.Core.has_string_representation,
            graph.string_literal(location),
        )

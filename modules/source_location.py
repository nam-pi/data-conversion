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
        self, graph: Nampi_graph, tables: Tables, source_label: str, location: str
    ):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the source location belongs to.
            tables (Tables): The data tables.
            source_label (str): The label of the source the source location belongs to.
            location (str): The location string (page name, url or similar).
        """
        super().__init__(graph, tables, Nampi_type.Core.source_location)
        source = Source(self._graph, self._tables, source_label)
        self.add_relationship(Nampi_type.Core.has_source, source)
        self.add_relationship(
            Nampi_type.Core.has_string_representation,
            Nampi_graph.string_literal(location),
        )

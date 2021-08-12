"""The module for the Source_location class.

Classes:
    Source_location
"""
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.source import Source
from modules.source_type import Source_type


class Source_location(Node):
    """A blank node with associated triples that represents a location in a source."""

    def __init__(self, graph: Nampi_graph, source: Source, location: str):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the source location belongs to.
            source: The source the location belongs to.
            location: The location string (page name, url or similar).
        """
        rdf_source_location = Nampi_type.Core.source_location
        rdf_source_type = Nampi_type.Core.has_source
        rdf_data_type = Nampi_type.Core.has_value
        if source.source_type == Source_type.ONLINE_RESOURCE:
            rdf_source_location = Nampi_type.Core.online_resource
            rdf_source_type = Nampi_type.Core.has_online_source
            rdf_data_type = Nampi_type.Core.has_url
        elif source.source_type == Source_type.MANUSCRIPT:
            rdf_source_location = Nampi_type.Mona.page
            rdf_source_type = Nampi_type.Mona.has_paged_source
            rdf_data_type = Nampi_type.Mona.has_page_number
        super().__init__(graph, rdf_source_location)
        self.add_relationship(rdf_source_type, source)
        self.add_relationship(
            rdf_data_type, Nampi_graph.string_literal(location))

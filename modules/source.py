"""The module for the Source class.

Classes:
    Source
    Source_type

"""
from __future__ import annotations

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource
from modules.source_type import Source_type


class Source(Resource):
    """A source RDF resource."""

    source_type: Source_type

    def __init__(self, graph: Nampi_graph, label: str, source_type: Source_type):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the source belongs to.
            label: The sources label.
            source_type: The source type.
        """
        self.source_type = source_type
        source_rdf_type = Nampi_type.Core.source
        if source_type == Source_type.ONLINE_RESOURCE:
            source_rdf_type = Nampi_type.Core.online_source
        elif source_type == Source_type.MANUSCRIPT:
            source_rdf_type = Nampi_type.Mona.manuscript
        super().__init__(graph, source_rdf_type, Nampi_ns.source, label)

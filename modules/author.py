"""The module for the Author class.

Classes:
    Author
"""
from __future__ import annotations

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Author(Resource):
    """An author RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        label: str,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the author belongs to.
            label: The authors label.
        """
        super().__init__(graph, Nampi_type.Core.author, Nampi_ns.author, label=label)

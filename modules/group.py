"""The module for the Group class.

Classes:
    Group
"""
from __future__ import annotations

from rdflib import URIRef

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.resource import Resource


class Group(Resource):
    """A group RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        group_type: URIRef,
        label: str,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the group belongs to.
            group_type: The URI of the group.
            label: The label for the group.
        """
        super().__init__(
            graph,
            group_type,
            Nampi_ns.groups,
            label,
        )

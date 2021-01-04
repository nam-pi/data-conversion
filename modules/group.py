"""The module for the Group class.

Classes:
    Group
"""
from __future__ import annotations

from typing import Optional

from rdflib import URIRef

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Group(Resource):
    """A group RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        label: str,
        group_type: Optional[URIRef] = None,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the group belongs to.
            label: The label for the group.
            group_type: The optional URI of the group.
        """

        super().__init__(
            graph,
            group_type if group_type else Nampi_type.Core.group,
            Nampi_ns.groups,
            label,
        )

"""The module for the Group class.

Classes:
    Group
"""
from __future__ import annotations

from typing import Optional, Dict
from modules.resource import Resource
from modules.person import Person
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from rdflib import URIRef


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
            group_type: The URI of the group
            label
        """
        super().__init__(
            graph,
            group_type,
            Nampi_ns.groups,
            label,
        )

"""The module for the Appellation class.

Classes:
    Appellation
"""
from enum import Enum, auto
from typing import Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.node import Node


class Appellation_type(Enum):
    """The available appellation types."""

    IDENTIFIER = auto()
    FAMILY_NAME = auto()
    GIVEN_NAME = auto()
    RELIGIOUS_NAME = auto()


class Appellation(Node):
    """An appellation."""

    def __init__(
        self,
        graph: Nampi_graph,
        text: str,
        appellation_type: Optional[Appellation_type] = Appellation_type.GIVEN_NAME,
    ):
        """Initialize the class.

        Parameters:
            graph: The graph.
            text: The text content of the appellation.
            appellation_type: The type of appellation.
        """
        if appellation_type == Appellation_type.IDENTIFIER:
            type_uri = Nampi_type.Core.identifier
            label = "Identifier"
        elif appellation_type == Appellation_type.FAMILY_NAME:
            type_uri = Nampi_type.Mona.family_name
            label = "Family name"
        elif appellation_type == Appellation_type.RELIGIOUS_NAME:
            type_uri = Nampi_type.Mona.religious_name
            label = "Religious name"
        else:
            type_uri = Nampi_type.Mona.given_name
            label = "Given name"

        super().__init__(graph, type_uri, Nampi_ns.aspect, label, True)
        self.add_relationship(
            Nampi_type.Core.has_xsd_string, self._graph.string_literal(text)
        )

"""The module for the Date class.

Classes:
    Date

"""
from __future__ import annotations

from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.node import Node


class Date(Node):
    """A blank node with associated triples that represents a date."""

    value: str = ""
    dateTime: str = ""

    def __init__(
        self,
        graph: Nampi_graph,
        value: str
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the date belongs to.
            value: A string in the format of YYYY-MM-DD that represents the date.
        """
        super().__init__(graph, Nampi_type.Core.date)
        literal = Nampi_graph.date_time_literal(value)
        self.value = value
        self.dateTime = str(literal)
        self.add_relationship(Nampi_type.Core.has_xsd_date_time, literal)

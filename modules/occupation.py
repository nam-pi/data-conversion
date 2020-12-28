"""The module for the Occupation class.

Classes:
    Occupation
"""
from typing import Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Occupation(Resource):
    """A Occupation resource."""

    def __init__(self, graph: Nampi_graph, label: Optional[str]) -> None:
        super().__init__(graph, Nampi_type.Core.occupation, Nampi_ns.occupations, label=label)

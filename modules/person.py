"""The module for the Person class.

Classes:
    Person
"""
from __future__ import annotations

from typing import Optional

from modules.gender import Gender
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Person(Resource):
    """A person RDF resource."""

    gender: Optional[Gender] = None
    gnd_id: Optional[str] = None

    def __init__(
        self,
        graph: Nampi_graph,
        label: str,
        gender: Optional[Gender] = None,
        gnd_id: Optional[str] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            label: The persons label.
            gender: The persons gender.
            gnd_id: The id of the person in the GND.
        """
        super().__init__(graph, Nampi_type.Core.person, Nampi_ns.persons, label=label)
        self.gender = gender
        self.gnd_id = gnd_id

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        label: Optional[str],
        gender: Optional[Gender] = None,
        gnd_id: Optional[str] = None,
    ) -> Optional[Person]:
        """Initialize the class if a valid label exists.

        Parameters:
            graph: The RDF graph the person belongs to.
            label: The persons label.
            gender: The persons gender.
            gnd_id: The id of the person in the GND.

        Returns:
            A Person object or None
        """
        return cls(graph, label, gender=gender, gnd_id=gnd_id) if label else None

"""The module for the Person class.

Classes:
    Person
    Gender
"""
from __future__ import annotations

from typing import Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.no_value import NoValue
from modules.resource import Resource
from modules.tables import Column, Table, Tables


def _map_gender(text: Optional[str]) -> Optional[Gender]:
    for _, member in Gender.__members__.items():
        if text == member.value:
            return member
    return None


class Gender(NoValue):
    """The gender of a person."""

    FEMALE = "F"
    MALE = "M"


class Person(Resource):
    """A person RDF resource."""

    gender: Optional[Gender]
    gnd_id: Optional[str]

    def __init__(self, graph: Nampi_graph, tables: Tables, label: str):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            label: The persons label.
        """
        super().__init__(
            graph, tables, Nampi_type.Core.person, Nampi_ns.persons, label=label
        )
        self.gender = _map_gender(
            tables.get_from_table(Table.PERSONS, Column.name, label, Column.gender)
        )
        self.gnd_id = tables.get_from_table(
            Table.PERSONS, Column.name, label, Column.gnd_id
        )

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        tables: Tables,
        label: Optional[str],
    ) -> Optional[Person]:
        """Initialize the class if a valid label exists.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            label: The persons label.

        Returns:
            A Person object or None
        """
        return cls(graph, tables, label) if label else None

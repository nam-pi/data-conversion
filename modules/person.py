"""The module for the Person class.

Classes:
    Person

"""

from __future__ import annotations

from typing import Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource
from modules.tables import Column, Tables, Table
from rdflib import BNode, Namespace, URIRef


class Person(Resource):
    """A person RDF resource."""

    gnd_id: Optional[str]

    def __init__(self, graph: Nampi_graph, tables: Tables, label: str):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the resource belongs to.
            tables (Tables): The data tables.
            label (str): The persons label.
        """
        super().__init__(
            graph, tables, Nampi_type.Core.person, Nampi_ns.persons, label=label
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
            graph (Nampi_graph): The RDF graph the resource belongs to.
            tables (Tables): The data tables.
            label (str): The persons label.

        Returns:
            Optional[Person]: A Person object or None
        """
        return cls(graph, tables, label) if label else None

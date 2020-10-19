"""The module for the Place class.

Classes:
    Place
"""
from __future__ import annotations

from typing import Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource
from modules.tables import Column, Tables, Table


class Place(Resource):
    """A person RDF resource."""

    geoname_id: Optional[str]
    wikidata_id: Optional[str]

    def __init__(self, graph: Nampi_graph, tables: Tables, label: str):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the place belongs to.
            tables: The data tables.
            label: The places label.
        """
        super().__init__(graph, tables, Nampi_type.Core.place, Nampi_ns.places, label)
        self.geoname_id = tables.get_from_table(
            Table.PLACES, Column.name, label, Column.geoname_id
        )
        self.wikidata_id = tables.get_from_table(
            Table.PLACES, Column.name, label, Column.wikidata
        )

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        tables: Tables,
        label: Optional[str],
    ) -> Optional[Place]:
        """Initialize the class if a valid label exists.

        Parameters:
            graph: The RDF graph the place belongs to.
            tables: The data tables.
            label: The places label.

        Returns:
            A Place object or None
        """
        return cls(graph, tables, label) if label else None

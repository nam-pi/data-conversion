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


class Place(Resource):
    """A person RDF resource."""

    geoname_id: Optional[str] = None
    wikidata_id: Optional[str] = None

    def __init__(
        self,
        graph: Nampi_graph,
        label: str,
        geoname_id: Optional[str] = None,
        wikidata_id: Optional[str] = None,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the place belongs to.
            label: The places label.
            geoname_id: The geoname id.
            wikidata_id: The wikidata id.
        """
        super().__init__(graph, Nampi_type.Core.place, Nampi_ns.place, label)
        self.geoname_id = geoname_id
        self.wikidata_id = wikidata_id

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        label: Optional[str],
        geoname_id: Optional[str] = None,
        wikidata_id: Optional[str] = None,
    ) -> Optional[Place]:
        """Initialize the class if a valid label exists.

        Parameters:
            graph: The RDF graph the place belongs to.
            label: The places label.
            geoname_id: The geoname id.
            wikidata_id: The wikidata id.

        Returns:
            A Place object or None
        """
        return (
            cls(graph, label, geoname_id=geoname_id, wikidata_id=wikidata_id)
            if label
            else None
        )

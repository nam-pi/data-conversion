"""The module for the Event class.

Classes:
    Event
"""
from __future__ import annotations

from typing import Optional

from modules.date import Date
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.place import Place
from modules.resource import Resource
from modules.tables import Column, Table, Tables
from rdflib import URIRef


class Event(Resource):
    """An event RDF resource."""

    date: Optional[Date]
    place: Optional[Place]

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        event_type: URIRef,
        label: Optional[str],
        date: Optional[Date],
        place: Optional[Place],
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            event_type: The type URI of the event
            label: An optional label for the event.
            date: The event date.
            place: The event place.
        """
        super().__init__(graph, tables, event_type, Nampi_ns.events, label)
        if place:
            self.place = place
            self.add_relationship(Nampi_type.Core.takes_place_at, place)
        if date:
            self.date = date
            if date.exact:
                relationship_type = Nampi_type.Core.takes_place_on
            elif not date.earliest:
                relationship_type = Nampi_type.Core.takes_place_before
            elif not date.latest:
                relationship_type = Nampi_type.Core.takes_place_after
            else:
                relationship_type = Nampi_type.Core.takes_place_sometime_between
            self.add_relationship(relationship_type, date)

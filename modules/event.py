"""The module for the Event class.

Classes:
    Event
"""
from __future__ import annotations

from typing import Optional, Type

from rdflib import URIRef

from modules.date import Date
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.person import Person
from modules.place import Place
from modules.resource import Resource


class Event(Resource):
    """An event RDF resource."""

    date: Optional[Date] = None
    main_person: Person
    place: Optional[Place] = None

    def __init__(
        self,
        graph: Nampi_graph,
        main_person: Person,
        main_person_relationship: Optional[URIRef] = None,
        label: str = "",
        event_type: Optional[URIRef] = None,
        date: Optional[Date] = None,
        place: Optional[Place] = None,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            event_type: The type URI of the event.
            main_person: The main person of the event.
            main_person_relationship: The main person relationship type reference.
            label: The event label.
            date: The event date.
            place: The event place.
        """
        super().__init__(
            graph,
            event_type if event_type else Nampi_type.Core.event,
            Nampi_ns.events,
            label,
            distinct=True
        )
        self.main_person = main_person

        if main_person_relationship:
            self.add_relationship(main_person_relationship, main_person)

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

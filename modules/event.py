"""The module for the Event class.

Classes:
    Event
"""
from __future__ import annotations

from typing import Optional

from rdflib import URIRef

from modules.date import Date
from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
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
        place: Optional[Place] = None,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the person belongs to.
            tables: The data tables.
            event_type: The type URI of the event.
            main_person: The main person of the event.
            main_person_relationship: The main person relationship type reference.
            label: The event label.
            place: The event place.
            exact_date: An optional string in the format of YYYY-MM-DD that represents the exact date.
            earliest_date: An optional string in the format of YYYY-MM-DD that represents the earliest possible date.
            latest_date: An optional string in the format of YYYY-MM-DD that represents the latest possible date.
        """
        super().__init__(
            graph,
            event_type if event_type else Nampi_type.Core.event,
            Nampi_ns.event,
            label,
            distinct=True
        )
        self.main_person = main_person

        if main_person_relationship:
            self.add_relationship(main_person_relationship, main_person)

        if place:
            self.place = place
            self.add_relationship(Nampi_type.Core.takes_place_at, place)

        if exact_date or earliest_date or latest_date:
            if exact_date:
                self.add_relationship(
                    Nampi_type.Core.takes_place_on, Date(graph, exact_date))
            else:
                if earliest_date:
                    self.add_relationship(
                        Nampi_type.Core.takes_place_not_earlier_than, Date(graph, earliest_date))
                if latest_date:
                    self.add_relationship(
                        Nampi_type.Core.takes_place_not_later_than, Date(graph, latest_date))

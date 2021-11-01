"""The module for the Death class.

Classes:
    Death
"""
from typing import Optional

from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place


class Burial(Event):
    """A burial event RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        buried_person: Person,
        place: Optional[Place] = None,
        exact_date: Optional[str] = None

    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the death belongs to.
            burried_person: The person that died in the event.
            place: The death place.
            exact_date: An optional string in the format of YYYY-MM-DD that represents the exact date.
            earliest_date: An optional string in the format of YYYY-MM-DD that represents the earliest possible date.
            latest_date: An optional string in the format of YYYY-MM-DD that represents the latest possible date.
        """
        super().__init__(
            graph,
            buried_person,
            Nampi_type.Mona.burial,
            place=place,
            exact_date=exact_date,
            label="Burial"
        )

"""The module for the Death class.

Classes:
    Death
"""
from typing import Optional

from modules.date import Date
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place


class Death(Event):
    """A death event RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        died_person: Person,
        death_date: Optional[Date] = None,
        death_place: Optional[Place] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the death belongs to.
            died_person: The person that died in the event.
            death_date: The death date.
            death_place: The death place.
        """
        super().__init__(
            graph,
            died_person,
            Nampi_type.Core.ends_life_of,
            date=death_date,
            place=death_place,
            label="Death"
        )

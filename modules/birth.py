"""The module for the Birth class.

Classes:
    Birth
"""
from typing import Optional

from modules.date import Date
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place


class Birth(Event):
    """A birth event RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        born_person: Person,
        birth_date: Optional[Date] = None,
        birth_place: Optional[Place] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the birth belongs to.
            born_person: The person born in the event.
            birth_date: The birth date
            birth_place: The birth place.
        """
        super().__init__(
            graph,
            Nampi_type.Core.birth,
            born_person,
            Nampi_type.Core.starts_life_of,
            date=birth_date,
            place=birth_place,
        )

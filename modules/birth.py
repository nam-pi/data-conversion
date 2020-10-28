"""The module for the Birth class.

Classes:
    Birth
"""
from typing import Optional

from modules.appellation import Appellation, Appellation_type
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
        birth_family_name_label: Optional[str] = None,
        birth_given_name_label: Optional[str] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the birth belongs to.
            born_person: The person born in the event.
            birth_date: The birth date
            birth_place: The birth place.
            birth_family_name_label: An optional family name.
            birth_given_name_label: An optional given name.
        """
        super().__init__(
            graph,
            born_person,
            Nampi_type.Core.starts_life_of,
            date=birth_date,
            place=birth_place,
        )
        if birth_family_name_label:
            birth_family_name = Appellation(
                self._graph, birth_family_name_label, Appellation_type.FAMILY_NAME
            )
            self.add_facet(
                Nampi_type.Core.assigns_appellation_to,
                Nampi_type.Core.assigns_appellation,
                birth_family_name,
            )
        if birth_given_name_label:
            birth_given_name = Appellation(
                self._graph, birth_given_name_label, Appellation_type.GIVEN_NAME
            )
            self.add_facet(
                Nampi_type.Core.assigns_appellation_to,
                Nampi_type.Core.assigns_appellation,
                birth_given_name,
            )

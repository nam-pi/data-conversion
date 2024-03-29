"""The module for the Birth class.

Classes:
    Birth
"""
from typing import List, Optional

from modules.appellation import Appellation, Appellation_type
from modules.aspect import Aspect
from modules.event import Event
from modules.family import Family
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place
from parsers.nampi_data_entry_form.nampi_data_entry_form import \
    family_member_label


class Birth(Event):
    """A birth event RDF resource."""

    @classmethod
    def __init_other_persons(
        cls, mother: Optional[Person], father: Optional[Person]
    ) -> List[Event.Person_definition]:
        definitions: List[Event.Person_definition] = []
        if mother:
            definitions.append(
                {"person": mother, "relationship": Nampi_type.Core.has_parent}
            )
        if father:
            definitions.append(
                {"person": father, "relationship": Nampi_type.Core.has_parent}
            )
        return definitions

    def __init__(
        self,
        graph: Nampi_graph,
        born_person: Person,
        place: Optional[Place] = None,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
        family_name_label: Optional[str] = None,
        given_name_label: Optional[str] = None,
        family_group_label: Optional[str] = None,
        mother: Optional[Person] = None,
        father: Optional[Person] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the birth belongs to.
            born_person: The person born in the event.
            place: The birth place.
            exact_date: An optional string in the format of YYYY-MM-DD that represents the exact date.
            earliest_date: An optional string in the format of YYYY-MM-DD that represents the earliest possible date.
            latest_date: An optional string in the format of YYYY-MM-DD that represents the latest possible date.
            family_name_label: An optional family name.
            given_name_label: An optional given name.
            family_group_label: An optional label for the family group
            mother: An optional person that is the born persons mother
            father: An optional person that is the born persons father
        """
        super().__init__(
            graph,
            born_person,
            Nampi_type.Core.starts_life_of,
            place=place,
            earliest_date=earliest_date,
            exact_date=exact_date,
            latest_date=latest_date,
            label="Birth",
            other_participants=Birth.__init_other_persons(mother, father),
        )
        if family_name_label:
            birth_family_name = Appellation(
                self._graph, family_name_label, Appellation_type.FAMILY_NAME
            )
            self.add_relationship(
                obj=birth_family_name, pred=Nampi_type.Core.adds_aspect
            )
        if given_name_label:
            birth_given_name = Appellation(
                self._graph, given_name_label, Appellation_type.GIVEN_NAME
            )
            self.add_relationship(
                obj=birth_given_name, pred=Nampi_type.Core.adds_aspect
            )
        if family_group_label:
            family = Family(self._graph, family_group_label)
            aspect = Aspect(self._graph, family_member_label)
            self.add_relationship(Nampi_type.Core.adds_aspect, aspect)
            self.add_relationship(Nampi_type.Core.changes_aspect_related_to, family)

"""The module for the Appellation_assignment class."""

from typing import Optional

from modules.appellation import Appellation, Appellation_type
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person


class Appellation_assignment(Event):
    """An event that solely assigns an appellation."""

    def __init__(
        self,
        graph: Nampi_graph,
        assignment_person: Person,
        assignment_text: str,
        appellation_type: Optional[Appellation_type] = Appellation_type.GIVEN_NAME,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the birth belongs to.
            assignment_person: The person the appellation is assigned to.
            assignment_text: The text content of the assignment.
            appellation_type: The type of appellation to assign.
        """

        appellation_name = "appellation"
        if appellation_type == Appellation_type.FAMILY_NAME:
            appellation_name = "family name"
        elif appellation_type == Appellation_type.GIVEN_NAME:
            appellation_name = "given name"
        elif appellation_type == Appellation_type.IDENTIFIER:
            appellation_name = "identifier"
        elif appellation_type == Appellation_type.RELIGIOUS_NAME:
            appellation_name = "religious name"

        person_type = Nampi_type.Core.changes_aspect_of
        appell_type = Nampi_type.Core.adds_aspect
        person_label = assignment_person.label
        assert person_label
        super().__init__(graph, assignment_person, person_type,
                         label="Assign " + appellation_name + " " + assignment_text)
        appellation = Appellation(graph, assignment_text, appellation_type)
        self.add_relationship(appell_type, appellation)

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

        person_type = Nampi_type.Core.assigns_name_to
        appell_type = Nampi_type.Core.assigns_name
        if appellation_type == Appellation_type.IDENTIFIER:
            raise Exception("Identifiers cannot be assigned")
        super().__init__(graph, assignment_person, person_type, label="Assign appellation")
        appellation = Appellation(graph, assignment_text, appellation_type)
        self.add_relationship(appell_type, appellation)

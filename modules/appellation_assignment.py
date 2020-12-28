"""The module for the Appellation_assignment class."""

from typing import Optional

from modules.appellation import Appellation, Appellation_type
from modules.date import Date
from modules.event import Event
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place


class Appellation_assignment(Event):
    """An event that solely assigns an appellation."""

    def __init__(
        self,
        graph: Nampi_graph,
        assignment_person: Person,
        assignment_text: str,
        appellation_type: Optional[Appellation_type] = Appellation_type.GIVEN_NAME,
        assignment_date: Optional[Date] = None,
        assignment_place: Optional[Place] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the birth belongs to.
            assignment_person: The person the appellation is assigned to.
            assignment_text: The text content of the assignment.
            appellation_type: The type of appellation to assign.
            assignment_date: The appellation assignment event date.
            assignment_place: The appellation assignment event place.
        """
        super().__init__(
            graph,
            assignment_person,
            Nampi_type.Core.assigns_appellation_to,
            date=assignment_date,
            place=assignment_place,
            label="Assign appellation"
        )
        appellation = Appellation(graph, assignment_text, appellation_type)
        self.add_relationship(Nampi_type.Core.assigns_appellation, appellation)

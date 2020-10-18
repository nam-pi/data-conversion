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
from modules.tables import Tables


class Birth(Event):
    """A birth event RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        person_label: str,
        exact_date: Optional[str],
        earliest_date: Optional[str],
        latest_date: Optional[str],
        event_place_label: Optional[str],
    ):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the person belongs to.
            tables (Tables): The data tables.
        """
        event_date = Date.optional(
            graph, tables, exact_date, earliest_date, latest_date
        )
        event_place = Place.optional(graph, tables, event_place_label)
        super().__init__(
            graph, tables, Nampi_type.Core.birth, "", event_date, event_place
        )
        person = Person(
            self._graph,
            self._tables,
            person_label,
        )
        self.add_relationship(Nampi_type.Core.starts_life_of, person)

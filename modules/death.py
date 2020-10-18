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
from modules.tables import Column, Tables
from pandas import Series


class Death(Event):
    """A death event RDF resource."""

    def __init__(self, graph: Nampi_graph, tables: Tables, row: Series) -> None:
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the death belongs to.
            tables (Tables): The data tables.
            row (Series): The data row for the death.
        """
        event_date = Date.optional(
            graph,
            tables,
            row[Column.exact_date],
            row[Column.earliest_date],
            row[Column.latest_date],
        )
        event_place = Place.optional(graph, tables, row[Column.event_place])
        super().__init__(
            graph, tables, Nampi_type.Core.death, "", event_date, event_place
        )
        person = Person(
            self._graph,
            self._tables,
            row[Column.person],
        )
        self.add_relationship(Nampi_type.Core.ends_life_of, person)

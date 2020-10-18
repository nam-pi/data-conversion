"""The module for the Date class.

Classes:
    Date

"""
from __future__ import annotations

import math
from numbers import Number
from typing import Any, Optional

from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.node import Node
from modules.tables import Tables
from rdflib import RDF


class Date(Node):
    """A blank node with associated triples that represents a date."""

    exact: Optional[str] = None
    earliest: Optional[str] = None
    latest: Optional[str] = None

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ) -> None:
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the date belongs to.
            tables (Tables): The data tables.
            exact_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the exact date.
            earliest_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the earliest possible date.
            latest_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the latest possible date.
        """
        if exact_date:
            super().__init__(graph, tables, Nampi_type.Core.date)
            self.exact = exact_date
            self.add_relationship(
                Nampi_type.Core.has_date_time_representation,
                Nampi_graph.date_time_literal(self.exact),
            )
        else:
            super().__init__(graph, tables, Nampi_type.Core.unclear_date)
            if earliest_date:
                self.earliest = earliest_date
                self.add_relationship(
                    Nampi_type.Core.has_earliest_possible_date_time_representation,
                    Nampi_graph.date_time_literal(self.earliest),
                )
            if latest_date:
                self.latest = latest_date
                self.add_relationship(
                    Nampi_type.Core.has_latest_possible_date_time_representation,
                    Nampi_graph.date_time_literal(self.latest),
                )

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        tables: Tables,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ) -> Optional[Date]:
        """Initialize the class if it can be meaningfully created from the provided input strings.

        Parameters:
            graph (Nampi_graph): The RDF graph the resource belongs to.
            tables (Tables): The data tables.
            exact_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the exact date.
            earliest_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the earliest possible date.
            latest_date (Optional[str] = None): An optional string in the format of YYYY-MM-DD that represents the latest possible date.

        Returns:
            Optional[Date]: A new date object if at least one of the provided values is a string, otherwise None.
        """
        return (
            cls(graph, tables, exact_date, earliest_date, latest_date)
            if exact_date or earliest_date or latest_date
            else None
        )

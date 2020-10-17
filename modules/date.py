from __future__ import annotations
from modules.node import Node
from typing import Optional, Any
from modules.nampi_graph import Nampi_graph
from modules.tables import Tables
from modules.rdf_types import Type
from rdflib import RDF
import math
from numbers import Number


class Date(Node):
    exact: Optional[str]
    earliest: Optional[str]
    latest: Optional[str]

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ) -> None:
        if self.valid_date(exact_date):
            super().__init__(graph, tables, Type.Core.date)
            self.exact = exact_date
            graph.add(
                self.node,
                Type.Core.has_date_time_representation,
                Nampi_graph.date_time_literal(self.exact),
            )
        else:
            super().__init__(graph, tables, Type.Core.unclear_date)
            if self.valid_date(earliest_date):
                self.earliest = earliest_date
                graph.add(
                    self.node,
                    Type.Core.has_earliest_possible_date_time_representation,
                    Nampi_graph.date_time_literal(self.earliest),
                )
            if self.valid_date(latest_date):
                self.latest = latest_date
                graph.add(
                    self.node,
                    Type.Core.has_latest_possible_date_time_representation,
                    Nampi_graph.date_time_literal(self.latest),
                )

    @staticmethod
    def valid_date(date: Any) -> str:
        if not date:
            return False
        if isinstance(date, Number):
            return False
        return True

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        tables: Tables,
        exact_date: Optional[str] = None,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ) -> Optional[Date]:
        return (
            cls(graph, tables, exact_date, earliest_date, latest_date)
            if cls.valid_date(exact_date)
            or cls.valid_date(earliest_date)
            or cls.valid_date(latest_date)
            else None
        )

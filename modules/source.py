"""The module for the Source class.

Classes:
    Source
    Source_type

"""
from __future__ import annotations

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.no_value import NoValue
from modules.resource import Resource
from modules.tables import Column, Table, Tables


def _map_source_type(text: str) -> Source_type:
    for _, member in Source_type.__members__.items():
        if text == member.value:
            return member
    raise ValueError("Could not find SourceType for '{}'".format(text))


class Source_type(NoValue):
    """Represents the source types."""

    MANUSCRIPT = "Manuscript"
    ONLINE_RESOURCE = "Online Resource"


class Source(Resource):
    """A source RDF resource."""

    source_type: Source_type

    def __init__(self, graph: Nampi_graph, tables: Tables, label: str):
        """Initialize the class.

        Parameters:
            graph (Nampi_graph): The RDF graph the source belongs to.
            tables (Tables): The data tables.
            label (str): The sources label.
        """
        super().__init__(graph, tables, Nampi_type.Core.source, Nampi_ns.sources, label)
        type = tables.get_from_table(
            Table.SOURCES, Column.title, label, Column.type  # type: ignore
        )
        if type:
            self.source_type = _map_source_type(type)

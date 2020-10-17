from __future__ import annotations
from modules.resource import Resource
from modules.tables import Tables, Col_heading
from modules.nampi_graph import Nampi_graph
from rdflib import URIRef, BNode, Namespace
from modules.rdf_types import Type
from modules.rdf_namespaces import Namespace as Nampi_ns
from modules.utils import get_df_value
from typing import Optional


class Person(Resource):
    gnd_id: Optional[str]

    def __init__(self, graph: Nampi_graph, tables: Tables, label: str):
        super().__init__(graph, tables, Type.Core.person, Nampi_ns.persons, label=label)
        self.gnd_id = get_df_value(
            tables.persons, Col_heading.name, label, Col_heading.gnd_id
        )

    @classmethod
    def optional(
        cls,
        graph: Nampi_graph,
        tables: Tables,
        label: Optional[str],
    ) -> Optional[Person]:
        return cls(graph, tables, label) if label else None

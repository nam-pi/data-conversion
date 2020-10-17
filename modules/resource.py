from rdflib import URIRef, BNode, Literal, Namespace, RDF, RDFS, XSD, Graph
from typing import Optional, List, TypeVar
from modules.node import Node
from modules.nampi_graph import Nampi_graph
from modules.tables import Tables


class Resource(Node):
    label: Optional[str]

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        type_uri: URIRef,
        ns: Optional[Namespace],
        label: Optional[str] = None,
    ) -> None:
        super().__init__(graph, tables, type_uri, ns, label)
        self.__label = label

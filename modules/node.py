from modules.tables import Tables
from modules.nampi_graph import Nampi_graph
from typing import Union, Optional
from rdflib import URIRef, BNode, Namespace


class Node:
    __graph: Nampi_graph
    __tables: Tables
    node: Union[URIRef, BNode]

    def __init__(
        self,
        graph: Nampi_graph,
        tables: Tables,
        type_uri: URIRef,
        ns: Optional[Namespace] = None,
        label: Optional[str] = None,
    ) -> None:
        self.__graph = graph
        self.__tables = tables
        if label and ns:
            self.node = self.__graph.add_labeled_resource(ns, type_uri, label)
        elif ns:
            self.node = self.__graph.add_named_resource(ns, type_uri)
        else:
            self.node = self.__graph.add_blind(type_uri)

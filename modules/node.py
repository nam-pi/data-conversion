"""The module for the Node class.

Classes:
    Node

"""
from typing import Optional, Union

from modules.nampi_graph import Nampi_graph
from modules.tables import Tables
from rdflib import BNode, Namespace, URIRef


class Node:
    """A node in the RDF graph. It is aware of the graph it belongs to and has access to the original source tables to use in initialization of node relationships."""

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
        """Initialize the class.

        Parameters:
        graph (Nampi_graph): The RDF graph the node belongs to.
        tables (Tables): The data tables.
        type_uri (URIRef): The URI of the nodes' type.
        ns (Optional[Namespace] = None): An optional namespace the nodes' URI will belong to.
        label (Optional[str] = None): An optional label for the node.
        """
        self.__graph = graph
        self.__tables = tables
        if label and ns:
            self.node = self.__graph.add_labeled_resource(ns, type_uri, label)
        elif ns:
            self.node = self.__graph.add_resource(ns, type_uri)
        else:
            self.node = self.__graph.add_blind(type_uri)

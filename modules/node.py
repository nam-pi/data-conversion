"""The module for the Node class.

Classes:
    Node

"""
from __future__ import annotations

from typing import Optional, Union

from modules.nampi_graph import Nampi_graph
from modules.tables import Tables
from rdflib import BNode, Literal, Namespace, URIRef


class Node:
    """A node in the RDF graph. It is aware of the graph it belongs to and has access to the original source tables to use in initialization of node relationships."""

    _graph: Nampi_graph
    _tables: Tables
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
            graph: The RDF graph the node belongs to.
            tables: The data tables.
            type_uri: The URI of the nodes' type.
            ns: An optional namespace the nodes' URI will belong to.
            label: An optional label for the node.
        """
        self._graph = graph
        self._tables = tables
        if label and ns:
            self.node = self._graph.add_labeled_resource(ns, type_uri, label)
        elif ns:
            self.node = self._graph.add_resource(ns, type_uri)
        else:
            self.node = self._graph.add_blind(type_uri)

    def add_relationship(
        self, pred: URIRef, obj: Union[Node, URIRef, BNode, Literal]
    ) -> None:
        """Add an relationship triple with the node as subject to the graph.

        Parameters:
            pred: The predicate for the resulting relationship.
            obj: The object node.
        """
        self._graph.add(
            self.node,
            pred,
            obj.node if hasattr(obj, "node") else obj,
        )

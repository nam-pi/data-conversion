"""The module for the Node class.

Classes:
    Node

"""
from __future__ import annotations

from typing import List, Optional, Union

from rdflib import BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

from modules.nampi_graph import Nampi_graph


class Node:
    """A node in the RDF graph."""

    _graph: Nampi_graph
    node: Union[URIRef, BNode]

    def __init__(
        self,
        graph: Nampi_graph,
        type_uri: Union[List[URIRef], URIRef],
        ns: Optional[Namespace] = None,
        label: Optional[str] = None,
        distinct: Optional[bool] = False
    ) -> None:
        """Initialize the class.

        Parameters:
            graph: The RDF graph the node belongs to.
            type_uri: The URI of the nodes' type.
            ns: An optional namespace the nodes' URI will belong to.
            label: An optional label for the node.
            distinct: An optional bool that signifies whether or not to consider the node as a distinct node that shouldn't be reused based on its label
        """
        self._graph = graph
        types: List[URIRef] = []
        if isinstance(type_uri, list):
            types = type_uri
        else:
            types.append(type_uri)
        if label and ns and not distinct:
            self.node = self._graph.add_labeled_resource(ns, types[0], label)
        elif ns:
            self.node = self._graph.add_resource(ns, types[0])
            if label:
                self.add_relationship(RDFS.label, Literal(label))
        else:
            self.node = self._graph.add_blind(types[0])
        if len(types) > 1:
            for type in types[1:]:
                self.add_relationship(RDF.type, type)

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
            getattr(obj, "node", obj),
        )

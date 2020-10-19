"""The module for the Resource class.

Classes:
    Resource
"""

from typing import List, Optional, TypeVar

from modules.nampi_graph import Nampi_graph
from modules.node import Node
from modules.tables import Tables
from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef


class Resource(Node):
    """A RDF resource resource with an individual uri and possibly a label."""

    label: Optional[str]

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
        graph: The RDF graph the resource belongs to.
        tables: The data tables.
        type_uri: The URI of the resources' type.
        ns: The namespace the resources' URI will belong to.
        label: An optional label for the resource.
        """
        super().__init__(graph, tables, type_uri, ns, label)
        self.label = label

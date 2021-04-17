"""The module for the Resource class.

Classes:
    Resource
"""

from typing import List, Optional, Union

from rdflib import Namespace, URIRef

from modules.nampi_graph import Nampi_graph
from modules.node import Node


class Resource(Node):
    """A RDF resource resource with an individual uri and possibly a label."""

    label: Optional[str] = None

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
        graph: The RDF graph the resource belongs to.
        type_uri: The URI of the resources' type.
        ns: The namespace the resources' URI will belong to.
        label: An optional label for the resource.
            distinct: An optional bool that signifies whether or not to consider the node as a distinct node that shouldn't be reused based on its label
        """
        super().__init__(graph, type_uri, ns, label, distinct)
        self.label = label

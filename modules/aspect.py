"""The module for the Occupation class.

Classes:
    Occupation
"""
from typing import List, Optional, Union

from rdflib.term import URIRef

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource


class Aspect(Resource):
    """An aspect resource."""

    def __init__(self, graph: Nampi_graph, label: Optional[str], type: Optional[Union[List[URIRef], URIRef]] = None) -> None:
        super().__init__(graph, type if type else Nampi_type.Core.aspect,
                         Nampi_ns.aspect, label=label)

"""The module for the Family class.

Classes:
    Family
"""

from modules.group import Group
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type


class Family(Group):
    """A family RDF resource."""

    def __init__(self, graph: Nampi_graph, label: str):
        """Initialize the class.

        Parameters:
            graph: the RDF graph the family belongs to.
            label: The label for the family.
        """
        super().__init__(graph, label=label, group_type=Nampi_type.Core.family)

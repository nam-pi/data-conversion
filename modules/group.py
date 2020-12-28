"""The module for the Group class.

Classes:
    Group
"""
from __future__ import annotations

from typing import Optional

from rdflib import URIRef

from modules.nampi_graph import Nampi_graph
from modules.nampi_ns import Nampi_ns
from modules.nampi_type import Nampi_type
from modules.resource import Resource

_types = {
    "Capuchin Order": Nampi_type.Mona.roman_catholic_order,
    "Carthusian Order": Nampi_type.Mona.roman_catholic_order,
    "Community Aggsbach": Nampi_type.Mona.carthusian_community,
    "Community Astheim": Nampi_type.Mona.carthusian_community,
    "Community Brno": Nampi_type.Mona.carthusian_community,
    "Community Gaming": Nampi_type.Mona.carthusian_community,
    "Community Valdice": Nampi_type.Mona.carthusian_community,
    "Community Žiče": Nampi_type.Mona.carthusian_community,
    "Dominican Order": Nampi_type.Mona.roman_catholic_order,
    "Parish Stein": Nampi_type.Mona.roman_catholic_parish,
    "Roman-Catholic Church": Nampi_type.Mona.christian_denomination,
    "Roman-Catholic order": Nampi_type.Mona.christian_order,
    "Roman-Catholic parish": Nampi_type.Mona.christian_parish,
    "Hermits": Nampi_type.Mona.roman_catholic_group,
    "Roman-Catholic community": Nampi_type.Mona.christian_community,
    "Diocesis of Lithuania": Nampi_type.Mona.roman_catholic_diocese,
    "Roman-Catholic diocesis": Nampi_type.Mona.christian_diocese,
    "Community Regensburg, Prüll": Nampi_type.Mona.carthusian_community,
    "Community Schnals": Nampi_type.Mona.carthusian_community,
    "Community Erfurt": Nampi_type.Mona.carthusian_community,
    "Community Olomouc": Nampi_type.Mona.carthusian_community,
    "Community Bistra": Nampi_type.Mona.carthusian_community,
    "Community Imbach": Nampi_type.Mona.dominican_community,
    "Community St. Laurenz Wien": Nampi_type.Mona.canonesses_of_st_augustine_community,
    "Canonesses of St. Augustin": Nampi_type.Mona.roman_catholic_order,
    "Community St. Jakob Wien": Nampi_type.Mona.canonesses_of_st_augustine_community,
    "Community Schwäbisch Gmünd": Nampi_type.Mona.dominican_community,
    "Community Tulln": Nampi_type.Mona.dominican_community,
    "Community Krems": Nampi_type.Mona.dominican_community,
    "Community Steyr": Nampi_type.Mona.dominican_community,
    "Community Augsburg": Nampi_type.Mona.dominican_community,
    "Community Münzbach": Nampi_type.Mona.dominican_community,
    "Community Windhaag": Nampi_type.Mona.dominican_community,
    "Community Strassburg": Nampi_type.Mona.dominican_community,
    "Community Dominicans Wien": Nampi_type.Mona.dominican_community,
    "Community Retz": Nampi_type.Mona.dominican_community,
    "Habersack": Nampi_type.Core.family,
    "Community Mauerbach": Nampi_type.Mona.carthusian_community,
    "Benedictine order": Nampi_type.Mona.roman_catholic_order,
    "Community Kleinmariazell": Nampi_type.Mona.benedictine_community,
    "Community Královo Pole": Nampi_type.Mona.carthusian_community,
    "Sprengseck": Nampi_type.Core.family,
    "Salburg": Nampi_type.Core.family,
    "Herberstein": Nampi_type.Core.family,
    "Thurn und Valsassina": Nampi_type.Core.family,
    "Wöber": Nampi_type.Core.family,
    "Otto (1)": Nampi_type.Core.family,
    "Otto (2)": Nampi_type.Core.family,
}


class Group(Resource):
    """A group RDF resource."""

    def __init__(
        self,
        graph: Nampi_graph,
        label: str,
        group_type: Optional[URIRef] = None,
    ):
        """Initialize the class.

        Parameters:
            graph: The RDF graph the group belongs to.
            label: The label for the group.
            group_type: The optional URI of the group.
        """

        super().__init__(
            graph,
            self.__map_label_to_type(label, group_type),
            Nampi_ns.groups,
            label,
        )

    def __map_label_to_type(self, label: str, group_type: Optional[URIRef]) -> URIRef:
        if group_type:
            return group_type
        mapped_type = _types[label]
        if mapped_type:
            return mapped_type
        else:
            raise Exception("Could not map '{}' to a type".format(label))

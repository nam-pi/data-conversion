"""The module for the Parser class.

Classes:
    Parser
"""

from typing import Optional

from modules.birth import Birth
from modules.date import Date
from modules.death import Death
from modules.di_act import Di_act
from modules.event import Event
from modules.gender import Gender
from modules.nampi_graph import Nampi_graph
from modules.person import Person
from modules.place import Place
from modules.source import Source
from modules.source_location import Source_location
from modules.source_type import Source_type
from modules.tables import Column, Table, Tables
from pandas import Series
from rdflib import Graph


class Parser:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    _tables: Tables
    _graph: Nampi_graph

    def __init__(self, tables: Tables):
        """Initialize the class.

        Parameters:
            tables (Tables): The data tables.
        """
        self._tables = tables
        self._graph = Nampi_graph()

    def parse(self) -> Graph:
        """Parse the input data and return the resulting RDF graph.

        Returns:
            The tabular data as RDF.
        """
        self.__add_births()
        self.__add_deaths()
        return self._graph.graph

    def __add_births(self):
        for _, row in self._tables.get_table(Table.BIRTHS).iterrows():
            born_person = self.__get_person(row[Column.person])
            if not born_person:
                return None
            birth_date = self.__get_date(
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            birth_place = self.__get_place(row[Column.event_place])
            birth = Birth(self._graph, born_person, birth_date, birth_place)
            self.__add_di_act(row, birth)

    def __add_deaths(self):
        for _, row in self._tables.get_table(Table.DEATHS).iterrows():
            died_person = self.__get_person(row[Column.person])
            if not died_person:
                return None
            death_date = self.__get_date(
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            death_place = self.__get_place(row[Column.event_place])
            death = Death(self._graph, died_person, death_date, death_place)
            self.__add_di_act(row, death)

    def __add_di_act(self, row: Series, event: Event):
        author = self.__get_person(row[Column.author])
        source_location = self.__get_source_location(
            row[Column.source], row[Column.source_location]
        )
        if not author:
            return None
        Di_act(
            self._graph,
            event,
            author,
            source_location,
            row[Column.interpretation_date],
            row[Column.comment],
        )

    def __get_date(
        self,
        exact_date: Optional[str],
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ) -> Optional[Date]:
        return Date.optional(
            self._graph,
            exact_date,
            earliest_date,
            latest_date,
        )

    def __get_person(self, person_label: Optional[str]) -> Optional[Person]:
        gender_text = self._tables.get_from_table(
            Table.PERSONS, Column.name, person_label, Column.gender
        )
        gender = None
        if gender_text == "M":
            gender = Gender.MALE
        elif gender_text == "F":
            gender = Gender.FEMALE
        gnd_id = self._tables.get_from_table(
            Table.PERSONS, Column.name, person_label, Column.gnd_id
        )
        return Person.optional(self._graph, person_label, gender=gender, gnd_id=gnd_id)

    def __get_place(self, place_label: Optional[str]) -> Optional[Place]:
        geoname_id = self._tables.get_from_table(
            Table.PLACES, Column.name, place_label, Column.geoname_id
        )
        wikidata_id = self._tables.get_from_table(
            Table.PLACES, Column.name, place_label, Column.wikidata
        )
        return Place.optional(
            self._graph, place_label, geoname_id=geoname_id, wikidata_id=wikidata_id
        )

    def __get_source_location(
        self, source_label: str, location_text: str
    ) -> Source_location:
        source_type_text = self._tables.get_from_table(
            Table.SOURCES, Column.title, source_label, Column.type
        )
        source_type = None
        if source_type_text == "Manuscript":
            source_type = Source_type.MANUSCRIPT
        elif source_type_text == "Online Resource":
            source_type = Source_type.ONLINE_RESOURCE
        if not source_type:
            raise ValueError(
                "Could not find source type for '{}'".format(source_type_text)
            )
        source = Source(self._graph, source_label, source_type)
        return Source_location(self._graph, source, location_text)

"""The module for the Nampi data entry form parser.

Classes:
    Nampi_data_entry_form
"""
from typing import Optional

import pandas
from modules.appellation import Appellation_type
from modules.appellation_assignment import Appellation_assignment
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
from parsers.nampi_data_entry_form.nampi_data_entry_form import Column
from parsers.nampi_data_entry_form.nampi_data_entry_form import (
    Nampi_data_entry_form as Sheet,
)
from parsers.nampi_data_entry_form.nampi_data_entry_form import Table
from pandas import Series
from rdflib import Graph


class Nampi_data_entry_form_parser:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    __sheet: Sheet
    _graph: Nampi_graph

    def __init__(
        self,
        graph: Nampi_graph,
        cache_path: str,
        credentials_path: str,
        cache_validity_days: int,
    ):
        """Initialize the class.

        Parameters:
            graph: The data graph.
        """
        self.__sheet = Sheet(cache_path, credentials_path, cache_validity_days)
        self._graph = graph

        print("\nParse the data for '{}'".format(self.__sheet.sheet_name))

        self.__add_persons()
        self.__add_births()
        self.__add_deaths()

        print("Finished parsing the data for '{}'".format(self.__sheet.sheet_name))

    def __add_births(self):
        for _, row in self.__sheet.get_table(Table.BIRTHS).iterrows():
            born_person = self.__get_person(row[Column.person])
            if not born_person:
                continue
            birth_date = self.__get_date(
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            birth_place = self.__get_place(row[Column.event_place])
            family_name_label = None
            if born_person.gender == Gender.MALE:
                family_name_label = self.__sheet.get_from_table(
                    Table.PERSONS, Column.name, born_person.label, Column.family_name
                )
            birth = Birth(
                self._graph,
                born_person,
                birth_date,
                birth_place,
                birth_family_name_label=family_name_label,
            )
            self.__insert_di_act(birth, row=row)
        print("\tParsed the births")

    def __add_deaths(self):
        for _, row in self.__sheet.get_table(Table.DEATHS).iterrows():
            died_person = self.__get_person(row[Column.person])
            if not died_person:
                continue
            death_date = self.__get_date(
                row[Column.exact_date],
                row[Column.earliest_date],
                row[Column.latest_date],
            )
            death_place = self.__get_place(row[Column.event_place])
            death = Death(self._graph, died_person, death_date, death_place)
            self.__insert_di_act(death, row=row)
        print("\tParsed the deaths")

    def __add_persons(self):
        for _, row in self.__sheet.get_table(Table.PERSONS).iterrows():
            source_label = row[Column.source]
            if not source_label:
                continue
            location_text = row[Column.source_location]
            person_label = row[Column.name]
            has_birth_event = self.__sheet.table_has_value(
                Table.BIRTHS,
                Column.person,
                person_label,
            )
            person = self.__get_person(row[Column.name])
            if not person:
                continue
            if not has_birth_event or person.gender == Gender.FEMALE:
                author_label = (
                    "Irene Rabl"
                    if source_label == "Professbuch Gaming 1604 - 1734"
                    else "Patrick Fiska"
                )
                family_name = row[Column.family_name]
                if family_name:
                    fn_assignment = Appellation_assignment(
                        self._graph,
                        person,
                        family_name,
                        Appellation_type.FAMILY_NAME,
                    )
                    self.__insert_di_act(
                        fn_assignment,
                        author_label=author_label,
                        source_label=source_label,
                        source_location_label=location_text,
                    )
                given_name = row[Column.given_name]
                if given_name:
                    bn_assignment = Appellation_assignment(
                        self._graph, person, given_name
                    )
                    self.__insert_di_act(
                        bn_assignment,
                        author_label=author_label,
                        source_label=source_label,
                        source_location_label=location_text,
                    )
        print("\tParsed the persons")

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
        gender_text = self.__sheet.get_from_table(
            Table.PERSONS, Column.name, person_label, Column.gender
        )
        gender = None
        if gender_text == "M":
            gender = Gender.MALE
        elif gender_text == "F":
            gender = Gender.FEMALE
        gnd_id = self.__sheet.get_from_table(
            Table.PERSONS, Column.name, person_label, Column.gnd_id
        )
        return Person.optional(self._graph, person_label, gender=gender, gnd_id=gnd_id)

    def __get_place(self, place_label: Optional[str]) -> Optional[Place]:
        geoname_id = self.__sheet.get_from_table(
            Table.PLACES, Column.name, place_label, Column.geoname_id
        )
        wikidata_id = self.__sheet.get_from_table(
            Table.PLACES, Column.name, place_label, Column.wikidata
        )
        return Place.optional(
            self._graph, place_label, geoname_id=geoname_id, wikidata_id=wikidata_id
        )

    def __get_source_location(
        self, source_label: str, location_text: str
    ) -> Source_location:
        source_type_text = self.__sheet.get_from_table(
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

    def __insert_di_act(
        self,
        event: Event,
        row: Series = pandas.Series(),
        author_label: str = "",
        source_label: str = "",
        source_location_label: str = "",
    ):
        author_label = row[Column.author] if Column.author in row else author_label
        source_label = row[Column.source] if Column.source in row else source_label
        source_location_label = (
            row[Column.source_location]
            if Column.source_location in row
            else source_location_label
        )
        author = self.__get_person(author_label)
        if not author:
            return None
        source_location = self.__get_source_location(
            source_label, source_location_label
        )
        interpretation_date = (
            row[Column.interpretation_date]
            if Column.interpretation_date in row
            else None
        )
        comment = row[Column.comment] if Column.comment in row else None
        Di_act(
            self._graph,
            event,
            author,
            source_location,
            interpretation_date,
            comment,
        )

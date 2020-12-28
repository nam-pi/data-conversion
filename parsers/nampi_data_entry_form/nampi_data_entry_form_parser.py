"""The module for the Nampi data entry form parser.

Classes:
    Nampi_data_entry_form
"""
import logging
from typing import Optional

import pandas
from modules.appellation import Appellation_type
from modules.appellation_assignment import Appellation_assignment
from modules.birth import Birth
from modules.date import Date
from modules.death import Death
from modules.di_act import Di_act
from modules.event import Event
from modules.family import Family
from modules.gender import Gender
from modules.group import Group
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place
from modules.source import Source
from modules.source_location import Source_location
from modules.source_type import Source_type
from modules.status import Status
from pandas import Series
from parsers.nampi_data_entry_form.nampi_data_entry_form import Column
from parsers.nampi_data_entry_form.nampi_data_entry_form import \
    Nampi_data_entry_form as Sheet
from parsers.nampi_data_entry_form.nampi_data_entry_form import Table


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

        logging.info("Parse the data for '{}'".format(self.__sheet.sheet_name))

        self.__add_persons()
        self.__add_births()
        self.__add_deaths()
        self.__add_complex_events()

        logging.info(
            "Finished parsing the data for '{}'".format(
                self.__sheet.sheet_name)
        )

    def __add_births(self):
        """
            Add all births from the births table including names and family group memberships.
        """
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
            family_names = [self.__sheet.get_from_table(Table.PERSONS, Column.name, born_person.label, Column.family_name_with_group), self.__sheet.get_from_table(
                Table.PERSONS, Column.name, born_person.label, Column.family_name_gender_neutral), self.__sheet.get_from_table(Table.PERSONS, Column.name, born_person.label, Column.family_name)]
            given_name_label = self.__sheet.get_from_table(
                Table.PERSONS, Column.name, born_person.label, Column.given_name
            )
            family_group_label = next(
                (s for s in family_names if s), None)
            birth = Birth(
                self._graph,
                born_person,
                birth_date,
                birth_place,
                birth_family_name_label=family_names[2],
                birth_given_name_label=given_name_label,
                birth_family_group_label=family_group_label
            )
            self.__insert_di_act(birth, row=row)
            logging.debug(
                "Added 'birth' for person '{}'".format(row[Column.person]))
        logging.info("Parsed the births")

    def __add_complex_events(self):
        """
            Add all complex events from the complex events table.
        """
        for _, row in self.__sheet.get_table(Table.COMPLEX_EVENTS).iterrows():
            person = self.__get_person(row[Column.person])
            if not person:
                continue
            definition = row[Column.event_definition]
            event = None

            def get_def_column(column: str):
                return self.__sheet.get_from_table(Table.EVENT_DEFINITIONS, Column.name, definition, column)

            def merge_event():
                nonlocal person, definition
                date = self.__get_date(
                    row[Column.exact_date],
                    row[Column.earliest_date],
                    row[Column.latest_date],
                )
                place = self.__get_place(row[Column.event_place])
                assert person is not None
                return Event(self._graph, person, date=date, place=place, label=definition)
            group_label = get_def_column(Column.status_occupation_in_group)
            group = Group(self._graph, group_label) if group_label else None
            added_status_label = get_def_column(Column.added_status)
            removed_status_label = get_def_column(Column.removed_status)
            if group and added_status_label:
                status = Status(self._graph, added_status_label)
                event = merge_event()
                event.add_relationship(
                    obj=person, pred=Nampi_type.Core.adds_group_status_to)
                event.add_relationship(
                    obj=group, pred=Nampi_type.Core.adds_group_status_in)
                event.add_relationship(
                    obj=status, pred=Nampi_type.Core.adds_group_status_as)
            if group and removed_status_label:
                status = Status(self._graph, removed_status_label)
                event = merge_event()
                event.add_relationship(
                    obj=person, pred=Nampi_type.Core.removes_group_status_from)
                event.add_relationship(
                    obj=group, pred=Nampi_type.Core.removes_group_status_in)
                event.add_relationship(
                    obj=status, pred=Nampi_type.Core.removes_group_status_as)
            if event:
                self.__insert_di_act(event, row=row)
            else:
                logging.warn("Skip event '{}' for person '{}'".format(
                    definition, person.label))
        logging.info("Parsed the complex events")

    def __add_deaths(self):
        """
            Add all death events from the deaths table.
        """
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
        logging.info("Parsed the deaths")

    def __add_persons(self):
        """
            Add all persons from the persons table not being added in birth events.
        """
        for _, row in self.__sheet.get_table(Table.PERSONS).iterrows():
            if not row[Column.source]:
                # Only use entries with source
                logging.warning(
                    "No source entry for 'person' table row '{}'".format(row[Column.name]))
                continue
            person_label = row[Column.name]
            has_birth_event = self.__sheet.table_has_value(
                Table.BIRTHS,
                Column.person,
                person_label,
            )
            person = self.__get_person(row[Column.name])
            if not person:
                continue
            if not has_birth_event:
                # Get all family name variants from the person table
                family_names = [row[Column.family_name_with_group],
                                row[Column.family_name_gender_neutral], row[Column.family_name]]
                # Get the official family name by looking through the ordered family_names list and picking the first match
                family_group_name = next(
                    (s for s in family_names if s), None)
                # Add family name group membership
                if family_group_name:
                    family = Family(self._graph, family_group_name)
                    become_member_event = Event(
                        self._graph, person, Nampi_type.Core.adds_group_status_to, label="Become family member")
                    become_member_event.add_relationship(
                        Nampi_type.Core.adds_group_status_as, Nampi_type.Core.family_member)
                    become_member_event.add_relationship(
                        Nampi_type.Core.adds_group_status_in, family)
                    self.__insert_di_act(become_member_event, row=row)
                    logging.debug("Added 'membership' in family '{}' for birthless person '{}'".format(
                        family.label, row[Column.name]))
                # Add names for persons that don't have birth events
                if family_names[2]:
                    # Add personal family name
                    fn_assignment = Appellation_assignment(
                        self._graph,
                        person,
                        family_names[2],
                        Appellation_type.FAMILY_NAME,
                    )
                    self.__insert_di_act(fn_assignment, row=row)
                if row[Column.given_name]:
                    # Add given name
                    gn_assignment = Appellation_assignment(
                        self._graph, person, row[Column.given_name]
                    )
                    self.__insert_di_act(gn_assignment, row=row)
                logging.debug(
                    "Added 'names' for birthless person '{}'".format(row[Column.name]))
        logging.info("Parsed the persons")

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

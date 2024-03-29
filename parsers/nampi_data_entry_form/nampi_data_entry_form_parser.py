"""The module for the Nampi data entry form parser.

Classes:
    Nampi_data_entry_form
"""
import logging
from typing import List, Optional

import pandas
from pandas import Series
from rdflib.term import URIRef

from modules.appellation import Appellation, Appellation_type
from modules.appellation_assignment import Appellation_assignment
from modules.aspect import Aspect
from modules.author import Author
from modules.birth import Birth
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
from modules.title import Title
from parsers.nampi_data_entry_form.nampi_data_entry_form import Column
from parsers.nampi_data_entry_form.nampi_data_entry_form import \
    Nampi_data_entry_form as Sheet
from parsers.nampi_data_entry_form.nampi_data_entry_form import (
    Table, added_investiture_label, family_member_label)

_group_types = {
    "Christian denomination": Nampi_type.Mona.christian_denomination,
    "Diocese": Nampi_type.Mona.diocese,
    "Family": Nampi_type.Mona.family,
    "Monastic community": Nampi_type.Mona.monastic_community,
    "Parish": Nampi_type.Mona.parish,
    "Polity": Nampi_type.Mona.polity,
    "Religious denomination": Nampi_type.Mona.religious_denomination,
    "Religious order": Nampi_type.Mona.religious_order,
    "Religious polity": Nampi_type.Mona.religious_polity,
    "Historic diocese": Nampi_type.Mona.historic_diocese,
}

_status_types = {
    "Academic degree": Nampi_type.Mona.academic_degree,
    "Clergy": Nampi_type.Mona.clergy,
    "Community subsacristan": Nampi_type.Mona.community_subsacristan,
    "Community superior": Nampi_type.Mona.community_superior,
    "Member of a religious community": Nampi_type.Mona.member_of_a_religious_community,
    "Member of a religious community with manual focus": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Member of a religious community with spiritual focus": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Procurator": Nampi_type.Mona.procurator,
    "Professed member of a religious community": Nampi_type.Mona.professed_member_of_a_religious_community,
    "Vice community superior": Nampi_type.Mona.vice_community_superior,
    "Visitator": Nampi_type.Mona.visitator,
    "Monastic office with spiritual focus": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Monastic office with manual focus": Nampi_type.Mona.monastic_office_with_manual_focus,
    "Monastic office": Nampi_type.Mona.monastic_office,
    "Member of a religious community visiting": Nampi_type.Mona.member_of_a_religious_community_visiting,
    "Religious life outside a community": Nampi_type.Mona.religious_life_outside_a_community,
    "Office in a diocese": Nampi_type.Mona.office_in_a_diocese,
    "Secular office": Nampi_type.Mona.secular_office,
    "Educator": Nampi_type.Mona.educator,
    "Office": Nampi_type.Mona.office,
    "Ruler of a school": Nampi_type.Mona.ruler_of_a_school,
    "Status": Nampi_type.Core.status,
    "Aspect": Nampi_type.Core.aspect,
    "Unspecified aspect": Nampi_type.Mona.unspecified_aspect,
}

_occupation_types = {
    "Administration of a community": Nampi_type.Mona.administration_of_a_community,
    "Associated parish clergy": Nampi_type.Mona.associated_parish_clergy,
    "Clergy": Nampi_type.Mona.clergy,
    "Official": Nampi_type.Mona.official,
    "Trade": Nampi_type.Mona.trade,
    "Rule of a community": Nampi_type.Mona.rule_of_a_community,
    "Monastic office": Nampi_type.Mona.monastic_office,
    "Secular office": Nampi_type.Mona.secular_office,
    "Office in a diocese": Nampi_type.Mona.office_in_a_diocese,
    "Office": Nampi_type.Mona.office,
    "Educator": Nampi_type.Mona.educator,
    "Servant": Nampi_type.Mona.servant,
    "Visitator": Nampi_type.Mona.visitator,
    "Highly skilled professional": Nampi_type.Mona.highly_skilled_professional,
    "Rule of a school": Nampi_type.Mona.rule_of_a_school,
    "Occupation": Nampi_type.Core.occupation,
    "Aspect": Nampi_type.Core.aspect,
    "Unspecified aspect": Nampi_type.Mona.unspecified_aspect,
}


def safe_str(row: Series, column: str) -> Optional[str]:
    return str(row[column]) if column in row else None


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
        self.__add_investiture_events_for_professions()
        self.__add_religious_names()
        self.__add_independent_titles()

        logging.info(
            "Finished parsing the data for '{}'".format(self.__sheet.sheet_name)
        )

    def __add_births(self):
        """
        Add all births from the births table including names and family group memberships.
        """
        for _, row in self.__sheet.get_table(Table.BIRTHS).iterrows():
            born_person = self.__get_person(safe_str(row, Column.person))
            if not born_person:
                continue
            mother = self.__get_person(safe_str(row, Column.mother))
            father = self.__get_person(safe_str(row, Column.father))
            birth_place = self.__get_place(safe_str(row, Column.event_place))
            family_names = [
                self.__sheet.get_from_table(
                    Table.PERSONS,
                    Column.name,
                    born_person.label,
                    Column.family_name_with_group,
                ),
                self.__sheet.get_from_table(
                    Table.PERSONS,
                    Column.name,
                    born_person.label,
                    Column.family_name_gender_neutral,
                ),
                self.__sheet.get_from_table(
                    Table.PERSONS, Column.name, born_person.label, Column.family_name
                ),
            ]
            given_name_label = self.__sheet.get_from_table(
                Table.PERSONS, Column.name, born_person.label, Column.given_name
            )
            family_group_label = next((s for s in family_names if s), None)
            birth = Birth(
                self._graph,
                born_person,
                birth_place,
                exact_date=safe_str(row, Column.exact_date),
                earliest_date=safe_str(row, Column.earliest_date),
                latest_date=safe_str(row, Column.latest_date),
                family_name_label=family_names[2],
                given_name_label=given_name_label,
                family_group_label=family_group_label,
                mother=mother,
                father=father,
            )
            self.__insert_di_act(birth, row=row)
            logging.debug(
                "Added 'birth' for person '{}'".format(birth.main_person.label)
            )
        logging.info("Parsed the births")

    def __add_complex_events(self):
        """
        Add all complex events from the complex events table.
        """
        for _, row in self.__sheet.get_table(Table.COMPLEX_EVENTS).iterrows():
            main_person = self.__get_person(safe_str(row, Column.person))
            if not main_person:
                continue
            definition = safe_str(row, Column.event_definition)
            event = None

            other_participant_labels: List[str] = []
            if Column.other_person_1 in row:
                other_participant_labels.append(str(row[Column.other_person_1]))
            if Column.other_person_2 in row:
                other_participant_labels.append(str(row[Column.other_person_2]))
            if Column.other_person_3 in row:
                other_participant_labels.append(str(row[Column.other_person_3]))
            if Column.other_person_4 in row:
                other_participant_labels.append(str(row[Column.other_person_4]))
            if Column.other_person_5 in row:
                other_participant_labels.append(str(row[Column.other_person_5]))
            other_participants: List[Event.Person_definition] = []
            for label in other_participant_labels:
                person = self.__get_person(label)
                if person:
                    other_participants.append({"person": person})

            def get_def_column(column: str):
                return self.__sheet.get_from_table(
                    Table.EVENT_DEFINITIONS, Column.name, definition, column
                )

            def merge_event():
                nonlocal event, main_person, definition
                if event:
                    return event
                place = self.__get_place(safe_str(row, Column.event_place))
                assert main_person is not None
                event = Event(
                    self._graph,
                    main_person,
                    place=place,
                    earliest_date=safe_str(row, Column.earliest_date),
                    exact_date=safe_str(row, Column.exact_date),
                    latest_date=safe_str(row, Column.latest_date),
                    label=str(definition),
                    other_participants=other_participants,
                )
                return event

            group_label = get_def_column(Column.status_occupation_in_group)
            group = self.__get_group(group_label)
            added_status_label = get_def_column(Column.added_status)
            removed_status_label = get_def_column(Column.removed_status)
            started_occupation_label = get_def_column(Column.started_occupation)
            stopped_occupation_label = get_def_column(Column.stopped_occupation)
            religious_title_text = get_def_column(Column.assigned_religious_title)

            if religious_title_text:
                e = merge_event()
                title = Title(
                    self._graph, religious_title_text, Nampi_type.Mona.religious_title
                )
                e.add_relationship(
                    obj=main_person, pred=Nampi_type.Core.has_main_participant
                )
                e.add_relationship(obj=title, pred=Nampi_type.Core.adds_aspect)

            if (
                added_status_label or started_occupation_label
            ) and added_status_label == started_occupation_label:
                aspect_label = added_status_label
                status_type = self.__get_status_type(added_status_label)
                occupation_type = self.__get_occupation_type(started_occupation_label)
                types: List[URIRef] = []
                if status_type:
                    types.append(status_type)
                if occupation_type:
                    types.append(occupation_type)
                aspect = Aspect(self._graph, aspect_label, types)
                e = merge_event()
                e.add_relationship(
                    obj=main_person, pred=Nampi_type.Core.has_main_participant
                )
                if group:
                    e.add_relationship(
                        obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                    )
                e.add_relationship(obj=aspect, pred=Nampi_type.Core.adds_aspect)
            else:
                if added_status_label:
                    type = self.__get_status_type(added_status_label)
                    aspect = Aspect(self._graph, added_status_label, type)
                    e = merge_event()
                    e.add_relationship(
                        obj=main_person, pred=Nampi_type.Core.has_main_participant
                    )
                    if group:
                        e.add_relationship(
                            obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                        )
                    e.add_relationship(obj=aspect, pred=Nampi_type.Core.adds_aspect)
                if started_occupation_label:
                    type = self.__get_occupation_type(started_occupation_label)
                    aspect = Aspect(self._graph, started_occupation_label, type)
                    e = merge_event()
                    e.add_relationship(
                        obj=main_person, pred=Nampi_type.Core.has_main_participant
                    )
                    e.add_relationship(obj=aspect, pred=Nampi_type.Core.adds_aspect)
                    if group:
                        e.add_relationship(
                            obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                        )

            if (
                removed_status_label or stopped_occupation_label
            ) and removed_status_label == stopped_occupation_label:
                aspect_label = removed_status_label
                status_type = self.__get_status_type(removed_status_label)
                occupation_type = self.__get_occupation_type(stopped_occupation_label)
                types: List[URIRef] = []
                if status_type:
                    types.append(status_type)
                if occupation_type:
                    types.append(occupation_type)
                aspect = Aspect(self._graph, aspect_label, types)
                e = merge_event()
                e.add_relationship(
                    obj=main_person, pred=Nampi_type.Core.has_main_participant
                )
                if group:
                    e.add_relationship(
                        obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                    )
                e.add_relationship(obj=aspect, pred=Nampi_type.Core.removes_aspect)
            else:
                if removed_status_label:
                    type = self.__get_status_type(removed_status_label)
                    aspect = Aspect(self._graph, removed_status_label, type)
                    e = merge_event()
                    e.add_relationship(
                        obj=main_person, pred=Nampi_type.Core.has_main_participant
                    )
                    if group:
                        e.add_relationship(
                            obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                        )
                    e.add_relationship(obj=aspect, pred=Nampi_type.Core.removes_aspect)
                if stopped_occupation_label:
                    type = self.__get_occupation_type(stopped_occupation_label)
                    aspect = Aspect(self._graph, stopped_occupation_label, type)
                    e = merge_event()
                    e.add_relationship(
                        obj=main_person, pred=Nampi_type.Core.has_main_participant
                    )
                    e.add_relationship(obj=aspect, pred=Nampi_type.Core.removes_aspect)
                    if group:
                        e.add_relationship(
                            obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                        )

            if event:
                self.__insert_di_act(event, row=row)
            else:
                logging.warn(
                    "Skip event '{}' for person '{}'".format(
                        definition, main_person.label
                    )
                )
        logging.info("Parsed the complex events")

    def __add_deaths(self):
        """
        Add all death events from the deaths table.
        """
        for _, row in self.__sheet.get_table(Table.DEATHS).iterrows():
            died_person = self.__get_person(safe_str(row, Column.person))
            if not died_person:
                continue
            death_place = self.__get_place(safe_str(row, Column.event_place))
            death = Death(
                self._graph,
                died_person,
                place=death_place,
                earliest_date=safe_str(row, Column.earliest_date),
                exact_date=safe_str(row, Column.exact_date),
                latest_date=safe_str(row, Column.latest_date),
            )
            self.__insert_di_act(death, row=row)
        logging.info("Parsed the deaths")

    def __add_independent_titles(self):
        title_query = """
            PREFIX core: <http://purl.org/nampi/owl/core#>
            PREFIX mona: <http://purl.org/nampi/owl/monastic-life#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?text
            WHERE {{
  	            ?event a core:event ;
                    core:assigns_title/core:has_xsd_string ?text ;
                    core:assigns_title_to/rdfs:label "{}" .
            }}
        """
        for _, row in self.__sheet.get_table(Table.PERSONS).iterrows():
            religious_title = safe_str(row, Column.religious_title)
            person_label = safe_str(row, Column.name)
            if religious_title:
                has_existing_title = bool(
                    self._graph.graph.query(title_query.format(person_label))
                )
                if not has_existing_title:
                    person = self.__get_person(person_label)
                    if person:
                        assert person_label
                        event = Event(
                            self._graph,
                            person,
                            label="Assign religious title " + religious_title,
                            main_person_relationship=Nampi_type.Core.has_main_participant,
                        )
                        title = Title(
                            self._graph,
                            religious_title,
                            Nampi_type.Mona.religious_title,
                        )
                        event.add_relationship(Nampi_type.Core.adds_aspect, title)
                        self.__insert_di_act(event, row)
                        logging.debug(
                            "Assigns title '{}' to '{}'".format(
                                religious_title, person_label
                            )
                        )
        logging.info("Finish adding independent titles")

    def __add_investiture_events_for_professions(self):
        """
        Add investiture events for persons that have specific profession events
        """
        professions_query = """
            PREFIX core: <http://purl.org/nampi/owl/core#>
            PREFIX mona: <http://purl.org/nampi/owl/monastic-life#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?author ?authoring_date ?source ?source_location ?group ?person_node ?person ?place ?exact_date ?earliest_date ?latest_date
            WHERE {
                ?event_node a core:event ;
                    rdfs:label ?event_label .
                ?dia_node core:has_interpretation ?event_node ;
                    core:is_authored_by/rdfs:label ?author ;
                    core:is_authored_on/core:has_date_time ?authoring_date ;
                    core:has_source_location ?source_node .
                ?source_node (core:has_source|core:has_online_source|mona:has_paged_source)/rdfs:label ?source ;
                    (core:has_value|core:has_text|core:has_url|mona:has_page_number) ?source_location .
                ?event_node core:changes_aspect_related_to/rdfs:label ?group ;
                    core:has_main_participant ?person_node .
                ?person_node rdfs:label ?person .
                OPTIONAL { ?event_node core:takes_place_at/rdfs:label ?place }
                OPTIONAL { ?event_node core:takes_place_on/core:has_date_time ?exact_date }
                OPTIONAL { ?event_node core:takes_place_not_later_than/core:has_date_time ?latest_date }
                OPTIONAL { ?event_node core:takes_place_not_earlier_than/core:has_date_time ?earliest_date }
                VALUES ?event_label { "Profession as choir monk in Astheim" "Profession as choir monk in Bistra" "Profession as choir monk in Gaming" "Profession as choir monk in Žiče" "Profession as choir nun in Imbach" "Profession as choir nun in St. Jakob" "Profession as converse in Gaming" "Profession as lay sister in Imbach" "Profession as priest monk in Gaming" "Profession as choir nun in St. Laurenz" "Profession as choir monk in Brno" "Second profession as choir nun in Imbach" "Secret profession as choir nun in Imbach" }
            }
        """
        has_investiture_event_query = """
            PREFIX core: <http://purl.org/nampi/owl/core#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            ASK WHERE {{
            ?event core:has_main_participant <{}> ;
                    rdfs:label ?label .
            FILTER ( CONTAINS(LCASE(?label), "investiture") )
            }}
        """
        for row in self._graph.graph.query(professions_query):
            has_investiture_event = bool(
                self._graph.graph.query(
                    has_investiture_event_query.format(row["person_node"])
                )
            )
            if not has_investiture_event:
                person = self.__get_person(str(row["person"]))
                if not person:
                    continue
                status_type = self.__get_status_type(added_investiture_label)
                aspect = Aspect(self._graph, added_investiture_label, status_type)
                author_label = str(row["author"])
                interpretation_date_text = str(row["authoring_date"]).partition("T")[0]
                source_label = str(row["source"])
                source_location_label = str(row["source_location"])
                group = self.__get_group(str(row["group"]))
                assert group is not None
                place = self.__get_place(str(row["place"]))
                exact_date = (
                    str(row["exact_date"]).partition("T")[0]
                    if row["exact_date"]
                    else None
                )
                earliest_date = (
                    str(row["earliest_date"]).partition("T")[0]
                    if row["earliest_date"]
                    else None
                )
                latest_date = (
                    str(row["latest_date"]).partition("T")[0]
                    if row["latest_date"]
                    else None
                )
                dates_sorted_by_specificity = [exact_date, latest_date, earliest_date]
                most_specific_date = next(
                    (s for s in dates_sorted_by_specificity if s), None
                )
                event = Event(
                    self._graph,
                    person,
                    main_person_relationship=Nampi_type.Core.has_main_participant,
                    place=place,
                    latest_date=most_specific_date,
                    label="Investiture in " + str(group.label),
                )
                event.add_relationship(
                    obj=group, pred=Nampi_type.Core.changes_aspect_related_to
                )
                event.add_relationship(obj=aspect, pred=Nampi_type.Core.adds_aspect)
                self.__insert_di_act(
                    event,
                    author_label=author_label,
                    source_label=source_label,
                    source_location_label=source_location_label,
                    interpretation_date_text=interpretation_date_text,
                )
                logging.debug(
                    "Added investiture event and interpretation for '{}'".format(
                        person.label
                    )
                )
        logging.info("Finished adding investiture events")

    def __add_persons(self):
        """
        Add all persons from the persons table not being added in birth events.
        """
        for _, row in self.__sheet.get_table(Table.PERSONS).iterrows():
            if not row[Column.source]:
                # Only use entries with source
                logging.warning(
                    "No source entry for 'person' table row '{}'".format(
                        row[Column.name]
                    )
                )
                continue
            person_label = safe_str(row, Column.name)
            has_birth_event = self.__sheet.table_has_value(
                Table.BIRTHS,
                Column.person,
                person_label,
            )
            person = self.__get_person(safe_str(row, Column.name))
            if not person:
                continue
            if not has_birth_event:
                # Get all family name variants from the person table
                family_names = [
                    safe_str(row, Column.family_name_with_group),
                    safe_str(row, Column.family_name_gender_neutral),
                    safe_str(row, Column.family_name),
                ]
                # Get the official family name by looking through the ordered family_names list and picking the first match
                family_group_name = next((s for s in family_names if s), None)
                # Add family name group membership
                if family_group_name:
                    family = Family(self._graph, family_group_name)
                    aspect = Aspect(self._graph, family_member_label)
                    become_member_event = Event(
                        self._graph,
                        person,
                        Nampi_type.Core.has_main_participant,
                        label="Become family member",
                    )
                    become_member_event.add_relationship(
                        Nampi_type.Core.adds_aspect, aspect
                    )
                    become_member_event.add_relationship(
                        Nampi_type.Core.changes_aspect_related_to, family
                    )
                    self.__insert_di_act(become_member_event, row=row)
                    logging.debug(
                        "Added 'membership' in family '{}' for birthless person '{}'".format(
                            family.label, row[Column.name]
                        )
                    )
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
                        self._graph, person, str(safe_str(row, Column.given_name))
                    )
                    self.__insert_di_act(gn_assignment, row=row)
                logging.debug(
                    "Added 'names' for birthless person '{}'".format(row[Column.name])
                )
        logging.info("Parsed the persons")

    def __add_religious_names(self):
        query = """
            PREFIX core: <http://purl.org/nampi/owl/core#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?event ?person ?person_label
            WHERE {
                ?event a core:event ;
                    rdfs:label ?label ;
                    core:has_main_participant ?person .
                ?person rdfs:label ?person_label
                FILTER (CONTAINS(LCASE(?label), "investiture"))
            }
            ORDER BY ?label
        """
        for row in self._graph.graph.query(query):
            person = row["person"]
            person_label = str(row["person_label"])
            investiture = row["event"]
            religious_name = self.__sheet.get_from_table(
                Table.PERSONS, Column.name, person_label, Column.religious_name
            )
            if religious_name:
                appellation = Appellation(
                    self._graph,
                    appellation_type=Appellation_type.RELIGIOUS_NAME,
                    text=religious_name,
                )
                self._graph.add(
                    investiture, Nampi_type.Core.adds_aspect, appellation.node
                )
                self._graph.add(
                    investiture, Nampi_type.Core.has_main_participant, person
                )
                logging.debug(
                    "Assigned religious name '{}' to '{}' in investiture".format(
                        religious_name, person_label
                    )
                )
        logging.info("Finished adding religious names to investitures")

    def __get_group(self, group_label: Optional[str]) -> Optional[Group]:
        if not group_label:
            return None
        group_type_label = self.__sheet.get_from_table(
            Table.GROUPS, Column.name, group_label, Column.type
        )
        part_of_label = self.__sheet.get_from_table(
            Table.GROUPS, Column.name, group_label, Column.part_of
        )
        group_type = (
            _group_types[group_type_label]
            if group_type_label
            else Nampi_type.Core.group
        )
        part_of_group = self.__get_group(part_of_label) if part_of_label else None
        group = Group(self._graph, group_label, group_type)
        if part_of_group:
            group.add_relationship(Nampi_type.Core.is_part_of, part_of_group)
        return group

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

    def __get_status_type(self, status_label):
        type_label = self.__sheet.get_from_table(
            Table.STATUSES, Column.name, status_label, Column.type
        )
        if type_label:
            if type_label in _status_types:
                return _status_types[type_label]
            else:
                logging.warning(
                    "No status type defined for label '{}'".format(type_label)
                )
        return None

    def __get_occupation_type(self, occupation_label):
        type_label = self.__sheet.get_from_table(
            Table.OCCUPATIONS, Column.name, occupation_label, Column.type
        )
        if type_label:
            if type_label in _occupation_types:
                return _occupation_types[type_label]
            else:
                logging.warning(
                    "No occupation type defined for label '{}'".format(type_label)
                )
        return None

    def __insert_di_act(
        self,
        event: Event,
        row: Series = pandas.Series(),
        author_label: str = "",
        source_label: str = "",
        source_location_label: str = "",
        interpretation_date_text: Optional[str] = None,
    ):
        source_label = row[Column.source] if Column.source in row else source_label
        source_location_label = (
            row[Column.source_location]
            if Column.source_location in row
            else source_location_label
        )
        source_location = self.__get_source_location(
            source_label, source_location_label
        )
        interpretation_date = (
            row[Column.interpretation_date]
            if Column.interpretation_date in row
            else interpretation_date_text
        )
        comment = row[Column.comment] if Column.comment in row else None
        if comment:
            event.add_comment(comment)
        Di_act(
            self._graph,
            event,
            ["Patrick Fiska", "Irene Rabl"],
            source_location,
            interpretation_date,
        )

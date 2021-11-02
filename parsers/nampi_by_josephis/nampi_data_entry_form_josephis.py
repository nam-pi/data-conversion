"""The module for the Nampi data entry form parser.

Classes:
    Nampi_data_entry_form
"""
import json
import logging
from datetime import date, datetime
from typing import List, Optional

import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials
from pandas import Series
from rdflib.term import URIRef

from modules.appellation import Appellation, Appellation_type
from modules.appellation_assignment import Appellation_assignment
from modules.aspect import Aspect
from modules.author import Author
from modules.birth import Birth
from modules.burial import Burial
from modules.date import Date
from modules.death import Death
from modules.di_act import Di_act
from modules.event import Event
from modules.family import Family
from modules.gettypesandstati import GetTypesAndStati
# from modules.gender import Gender
from modules.group import Group
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place
from modules.source import Source
from modules.source_location import Source_location
from modules.source_type import Source_type
from modules.title import Title
from parsers.nampi_by_josephis.classes.entity_importer_josephis import \
    Entity_Importer_Josephis
from parsers.nampi_by_prodomo.classes.date import Dates
from parsers.nampi_data_entry_form.nampi_data_entry_form import (
    Table, added_investiture_label, family_member_label)

_types = dict(
    Geburt="Geburt",
    Abt="Abt",
    Beerdigung="Beerdigung",
    Beziehung="Beziehung",
    Bischof="Bischof",
    Geschwister="Geschwister",
    Konvent="Konvent",
    Pfarrvikar="Pfarrvikar",
    Priester="Priester",
    Subdiakon="Subdiakon",
    Taufe="Taufe",
    Tod="Tod",
)

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

authors = ["Stephan Makowski", "Manuela Mayer", "Mag. Andrea Singh Bottanova, MA"]


def safe_str(row: Series, column: str) -> Optional[str]:
    return str(row[column]) if column in row else None


Entities_dict = {}


class Nampi_data_entry_form_parser_josephis:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    _graph: Nampi_graph
    _stati: {}
    _occupation: {}

    # Get all Entries from Group_Entities Spreadsheet
    def getEntities(self):
        logging.info("Getting Group_Entites")

        # Extract and print all of the values
        list_of_hashes = GetTypesAndStati("Josephis").getData()
        print("--Start analyzing 'Josephis_Überarbeitungsformular_ASB' --")
        i = 0
        for val in list_of_hashes:
            Entry = Entity_Importer_Josephis()
            Entry.ExactCite = val["Exaktes Zitat"]
            Entry.Enable = val["Aufnehmen (x)"].strip()
            Entry.RelTitle = val["Religious title"]
            Entry.Forename = val["Vorname(n)"]
            Entry.Surename = val["Nachname"]
            Entry.Deathdate = val["Todesdatum"]
            Entry.Deathdateearly = val["Todesdatum (frühest)"]
            Entry.Deathdatelate = val["Todesdatum (spätest)"]
            Entry.Deathplace = val["Todesort"]
            Entry.DeathplaceGeo = val["geonames Todesort (populated place)"]
            Entry.IssuePlace = val["Wirkungsort"]
            Entry.IssuePlacegeo = val["geonames Wirkungsort (populated place)"]
            Entry.Community = val["Group/Community"]
            Entry.Status = val["Status (mehrere durch % trennen)"]
            Entry.Status_Nampi = val["Status_nampi (name)"]
            Entry.Occupation = val["Occupation (mehrere durch % trennen)"]
            Entry.Occupation_Nampi = val["Occupation_nampi (name)"]
            Entry.Event = val["Eventdefinition_nampi (name)"]
            Entry.Cite = val["Zitation (Jahr und Tagesdatum)"]
            Entry.GND = val["GND"]
            Entry.Comment = val["Kommentar"]
            Entry.Source = val["Quellenangabe"]

            Entities_dict[i] = Entry
            i = i + 1

        logging.info("Finished Getting Group_Entities")
        print("--Ready with 'Josephis_Überarbeitungsformular_ASB' --")

    def createJosephis(self):
        print("-- Create entries --")
        logging.info("-- Create entries --")
        for index in Entities_dict:
            Entry = Entity_Importer_Josephis()
            Entry = Entities_dict[index]

            # Just do stuff, if Enable == "X"
            if Entry.Enable.upper() == "X":

                # Person
                Comment = Entry.Comment
                persName = Entry.Forename + " " + Entry.Surename
                print("Create entry: " + persName)
                logging.info("-- Create entry: --" + persName)
                person = self.__get_person(persName, Entry.GND)
                if Comment:
                    person.add_comment(Comment)

                # check if Deathdate is valid
                date = Entry.Deathdate
                datefirst = Entry.Deathdateearly
                datelast = Entry.Deathdatelate

                # Geburt / inits
                family_names = Entry.Surename
                date_value = ""

                # Exaktes Datum ist vorhanden. Ansonsten letzt verfügbares Datum nehmen
                if len(date) > 0:
                    date_value = date
                elif len(datelast) > 0:
                    date_value = datelast

                birth = Birth(
                    self._graph,
                    person,
                    latest_date=date_value,
                    family_name_label=family_names,
                )
                birth.add_text(Entry.ExactCite, "la")
                self.__insert_di_act(
                    birth,
                    (),
                    authors,
                    Entry.Source,
                    Entry.Cite,
                    self._d1,
                )
                family = Family(self._graph, family_names)
                aspect = Aspect(self._graph, family_names)

                # Nur wenn Nachname gefüllt
                if len(family_names) != 0:
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
                    logging.debug("Added 'membership' in family ")

                    self.__insert_di_act(
                        become_member_event,
                        (),
                        authors,
                        Entry.Source,
                        Entry.Cite,
                        self._d1,
                    )

                # Tod

                # Exaktes Datum / Datum frühestens / Datum spätestens
                death = self.add_deaths(
                    persName,
                    (),
                    Entry.Deathplace,
                    Entry.DeathplaceGeo,
                    Entry.Cite,
                    datefirst,
                    date,
                    datelast,
                    Entry.Source,
                )

                # Wenn Event vorhanden, schreiben
                if death:
                    death.add_text(Entry.ExactCite, "la")
                    self.__insert_di_act(
                        death,
                        (),
                        authors,
                        Entry.Source,
                        Entry.Cite,
                        self._d1,
                    )

                cite = Entry.Cite
                # Titel
                if Entry.RelTitle:
                    RelTitle = Event(
                        self._graph,
                        person,
                        latest_date=date,
                    )
                    RelTitle.add_text(Entry.ExactCite, "la")
                    title = Title(
                        self._graph, Entry.RelTitle, Nampi_type.Mona.religious_title
                    )

                    RelTitle.add_relationship(
                        obj=person, pred=Nampi_type.Core.has_main_participant
                    )
                    RelTitle.add_relationship(
                        obj=title, pred=Nampi_type.Core.adds_aspect
                    )
                    self.__insert_di_act(
                        RelTitle,
                        (),
                        authors,
                        Entry.Source,
                        Entry.Cite,
                        self._d1,
                    )

                # Inits
                PlaceArray = ""
                PlaceGeoArray = ""
                GroupArray = ""
                StatusArray = ""
                StatusNampiArray = ""
                OccupationArray = ""
                OccupationNampiArray = ""
                EventArray = ""

                # Place
                if Entry.IssuePlace.find("%"):
                    PlaceArray = Entry.IssuePlace.split("%")

                if str(Entry.IssuePlacegeo).find("%"):
                    PlaceGeoArray = str(Entry.IssuePlacegeo).split("%")

                # Community
                if Entry.Community.find("%"):
                    GroupArray = Entry.Community.split("%")

                # Status
                if Entry.Status.find("%"):
                    StatusArray = Entry.Status.split("%")

                # Status Nampi
                if Entry.Status_Nampi.find("%"):
                    StatusNampiArray = Entry.Status_Nampi.split("%")

                # Occupation
                if Entry.Occupation.find("%"):
                    OccupationArray = Entry.Occupation.split("%")

                # Occupation_Nampi
                if Entry.Occupation_Nampi.find("%"):
                    OccupationNampiArray = Entry.Occupation_Nampi.split("%")

                # Event
                if Entry.Event.find("%"):
                    EventArray = Entry.Event.split("%")

                for (i, val) in enumerate(GroupArray):

                    Group = self.__get_group(
                        "Monastic community",
                        GroupArray[i].replace('"', ""),
                        GroupArray[i].replace('"', ""),
                    )

                    if len(PlaceArray) > i and len(PlaceGeoArray) > i:
                        Place = self.__get_place(
                            PlaceArray[i].strip(), PlaceGeoArray[i].split(" ")[0]
                        )
                        strPlace = PlaceArray[i].strip()
                    elif len(PlaceArray) > 0 and len(PlaceGeoArray) > 0:
                        Place = self.__get_place(
                            PlaceArray[-1].strip(), PlaceGeoArray[-1].split(" ")[0]
                        )
                        strPlace = PlaceArray[-1].strip()
                    else:
                        Place = ""
                        strPlace = ""

                    if len(EventArray) > i:
                        varEvent = EventArray[i]
                    elif len(EventArray) > 0:
                        varEvent = EventArray[-1]
                    else:
                        varEvent = ""

                    if len(StatusArray) > i:
                        varStatus = StatusArray[i]
                    elif len(StatusArray) > 0:
                        varStatus = StatusArray[-1]
                    else:
                        varStatus = ""

                    if len(StatusNampiArray) > i:
                        varStatusNampi = StatusNampiArray[i]
                    elif len(StatusNampiArray) > 0:
                        varStatusNampi = StatusNampiArray[-1]
                    else:
                        varStatusNampi = ""

                    varStatusNampi = varStatusNampi.strip()
                    if len(OccupationArray) > i is not None:
                        varOccupation = OccupationArray[i]
                    elif len(OccupationArray) > 0:
                        varOccupation = OccupationArray[-1]

                    if len(OccupationNampiArray) > i is not None:
                        varOccupation_Nampi = OccupationNampiArray[i]
                    elif len(OccupationNampiArray) > 0:
                        varOccupation_Nampi = OccupationNampiArray[-1]

                    if len(varStatusNampi.strip()) > 0:

                        if self._stati.getValues()[varStatusNampi.strip()]["Type"]:
                            type = self._stati.getValues()[varStatusNampi.strip()][
                                "Type"
                            ]

                            varStatusType = _status_types[type]

                        # if self._occupation.getValues()[varStatusNampi.strip()]["Type"]:
                        #     type = self._stati.getValues()[varOccupation_Nampi.strip()]["Type"]

                        #     varOccupationType = _occupation_types[type]

                    event = None

                    if len(date) > 0:

                        event = Event(
                            self._graph,
                            person,
                            Nampi_type.Core.has_main_participant,
                            varEvent,
                            (),
                            Place,
                            latest_date=date,
                        )
                        event.add_text(Entry.ExactCite, "la")

                    elif len(datelast) > 0:

                        event = Event(
                            self._graph,
                            person,
                            Nampi_type.Core.has_main_participant,
                            varEvent,
                            (),
                            Place,
                            earliest_date=datefirst,
                            latest_date=datelast,
                        )
                        event.add_text(Entry.ExactCite, "la")

                    aspect_label = ""
                    occupation_type = ""
                    if (
                        varStatusNampi or varOccupation_Nampi
                    ) and varStatusNampi == varOccupation_Nampi:
                        aspect_label == varOccupation_Nampi
                        status_type = varStatusType
                        occupation_type = ""  # varOccupationType
                        types: List[URIRef] = []
                        if status_type:
                            types.append(status_type)
                        if occupation_type:
                            types.append(occupation_type)

                        if event is not None:
                            aspect = Aspect(self._graph, aspect_label, types)

                            event.add_relationship(
                                obj=person, pred=Nampi_type.Core.has_main_participant
                            )
                            if Group:
                                event.add_relationship(
                                    obj=Group,
                                    pred=Nampi_type.Core.changes_aspect_related_to,
                                )
                            event.add_relationship(
                                obj=aspect, pred=Nampi_type.Core.adds_aspect
                            )
                    else:
                        if len(varStatusNampi.strip()) > 0:
                            status_type = varStatusType
                            aspect_label == varOccupation_Nampi
                            if event is not None:

                                if status_type is None:
                                    status_type = Nampi_type.Core.aspect

                                aspect = Aspect(
                                    self._graph, varStatusNampi, status_type
                                )
                                event.add_relationship(
                                    obj=person,
                                    pred=Nampi_type.Core.has_main_participant,
                                )
                                if Group:
                                    event.add_relationship(
                                        obj=Group,
                                        pred=Nampi_type.Core.changes_aspect_related_to,
                                    )
                                event.add_relationship(
                                    obj=aspect, pred=Nampi_type.Core.adds_aspect
                                )

                        elif varOccupation_Nampi:
                            occupation_type = ""  # varOccupationType
                            if event is not None:
                                aspect = Aspect(
                                    self._graph, varOccupation_Nampi, occupation_type
                                )
                                event.add_relationship(
                                    obj=person,
                                    pred=Nampi_type.Core.has_main_participant,
                                )
                                if Group:
                                    event.add_relationship(
                                        obj=Group,
                                        pred=Nampi_type.Core.changes_aspect_related_to,
                                    )
                                event.add_relationship(
                                    obj=aspect, pred=Nampi_type.Core.adds_aspect
                                )

                    if event:
                        self.__insert_di_act(
                            event,
                            (),
                            authors,
                            Entry.Source,
                            cite,
                            self._d1,
                        )

                print("Create entry: " + persName + " ready")

    def __init__(self, graph: Nampi_graph):
        """Initialize the class.

        Parameters:
            graph: The data graph.
        """
        self._graph = graph
        today = date.today()
        self._d1 = today.strftime("%Y-%m-%d")
        self._stati = GetTypesAndStati("Statuses")
        self._occu = GetTypesAndStati("Occupations")
        self.getEntities()

    def add_deaths(
        self,
        singleperson,
        deathday,
        deathplace,
        deathgeo,
        cite,
        deathearlist,
        deathexact,
        deathlatest,
        source,
    ):
        """
        Add all death events from the deaths table.
        """

        died_person = self.__get_person(singleperson, ())

        if not died_person:
            return
        death_place = self.__get_place(deathplace.strip(), deathgeo)

        if len(deathday) > 0:
            death = Death(self._graph, died_person, death_place, exact_date=deathexact)
        elif len(deathlatest) > 0:
            death = Death(
                self._graph,
                died_person,
                death_place,
                earliest_date=deathearlist,
                latest_date=deathlatest,
            )
        else:
            death = None

        if death:
            self.__insert_di_act(
                death,
                (),
                authors,
                source,
                cite,
                self._d1,
            )

        logging.info("Parsed the deaths")

    def __get_group(
        self, group_type_desc, group_label: Optional[str], part_of_label
    ) -> Optional[Group]:
        if not group_label:
            return None
        group_type_label = group_label
        group_type = _group_types[group_type_desc]
        part_of_group = (
            self.__get_group(part_of_label, (), ()) if part_of_label else None
        )
        group = Group(self._graph, group_label, group_type)
        if part_of_group:
            group.add_relationship(Nampi_type.Core.is_part_of, part_of_group)
        return group

    def __get_person(
        self, person_label: Optional[str], gnd_id: Optional[str]
    ) -> Optional[Person]:

        if gnd_id and str(gnd_id).upper() != "KEINE":
            if str(gnd_id).find(" "):
                gnd_split = str(gnd_id).split(" ")
                gnd_id_split = gnd_split[0]
                gnd = "http://d-nb.info/gnd/" + str(gnd_id_split).strip()
            else:
                gnd = "http://d-nb.info/gnd/" + str(gnd_id).strip()
        else:
            gnd = ""
        gender = ""

        return Person.optional(self._graph, person_label, gender, gnd)

    def __get_place(
        self, place_label: Optional[str], geoid: Optional[str]
    ) -> Optional[Place]:
        if geoid:
            geoname_id = str(geoid).strip()
        else:
            geoname_id = ""

        place_label = place_label.replace('"', "")
        return Place.optional(self._graph, place_label.strip(), geoname_id, "")

    def __get_source_location(
        self, source_label: str, location_text: Optional[str]
    ) -> Source_location:
        source_type_text = "Manuscript"
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
        if len(location_text) > 0:
            return Source_location(self._graph, source, location_text)
        else:
            return source

    def __insert_di_act(
        self,
        event: Event,
        row: Series = pandas.Series(),
        author_label: str = "",
        source_label: str = "",
        source_location_label: str = "",
        interpretation_date_text: Optional[str] = None,
    ):
        author_label = author_label
        source_label = source_label
        source_location_label = source_location_label

        author = author_label  # Author(self._graph, author_label)
        if not author:
            return None
        source_location = self.__get_source_location(
            source_label, source_location_label
        )
        interpretation_date = interpretation_date_text

        comment = None
        if comment:
            event.add_comment(comment)
        Di_act(
            self._graph,
            event,
            author,
            source_location,
            interpretation_date,
        )

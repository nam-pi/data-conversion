"""The module for the Nampi data entry form parser.

Classes:
    Nampi_data_entry_form
"""
import logging
import json
from datetime import date
from typing import List, Optional
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
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

# from modules.gender import Gender
from modules.group import Group
from modules.nampi_graph import Nampi_graph
from modules.nampi_type import Nampi_type
from modules.person import Person
from modules.place import Place
from modules.source import Source
from modules.source_location import Source_location
from modules.source_type import Source_type

# from modules.title import Title
from pandas import Series
from parsers.nampi_by_prodomo.classes.date import Dates
from parsers.nampi_by_prodomo.classes.entity_importer import Entity_Importer
from parsers.nampi_data_entry_form.nampi_data_entry_form import (
    Table,
    added_investiture_label,
    family_member_label,
)

from rdflib.term import URIRef

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
}

_occupation_types = {
    "Administration of a community": Nampi_type.Mona.administration_of_a_community,
    "Associated parish clergy": Nampi_type.Mona.associated_parish_clergy,
    "Clergy": Nampi_type.Mona.clergy,
    "Official": Nampi_type.Mona.official,
    "Profession": Nampi_type.Mona.profession,
    "Rule of a community": Nampi_type.Mona.rule_of_a_community,
}


def safe_str(row: Series, column: str) -> Optional[str]:
    return str(row[column]) if column in row else None


Entities_dict = {}


class Nampi_data_entry_form_parser_prodomo:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    _graph: Nampi_graph

    # Get all Entries from Group_Entities Spreadsheet
    def getEntities(self):
        # use creds to create a client to interact with the Google Drive API
        # scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(".credentials.json")
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        sheet = client.open("Group_Entities").sheet1

        # Extract and print all of the values
        list_of_hashes = sheet.get_all_records()
        print("--Start analyzing Group_Entities--")
        
        for i in list_of_hashes:
            Entry = Entity_Importer()
            Entry.Key = i["Rule"].strip()
            Entry.Label = i["NAMPI Label"]
            Entry.Event = i["Name (für Event-Labels)"]
            Entry.AspectPart = i["Aspect-Part"]
            Entry.Class = i["NAMPI Klasse"]
            Entry.Part_Of_Label = i["part of Label"]
            Entry.Place_Label = i["Label für Event-Orte im Kloster"]
            Entry.GeoId = i["Geonames-Id für Events im Kloster"]
            Entities_dict[i["Rule"].strip()] = Entry

        print("--Ready with Group_Entities--")

    def __init__(self, graph: Nampi_graph):
        """Initialize the class.

        Parameters:
            graph: The data graph.
        """
        self._graph = graph
        today = date.today()
        self._d1 = today.strftime("%Y-%m-%d")
        self.getEntities()

    def __add_births(
        self, date, person_label, family, birthplace, id, _mother, _father
    ):
        """
        Add all births from the births table including names and family group memberships.
        """
        logging.debug(date)
        if date and birthplace:
            born_person = self.__get_person(person_label)
            if born_person:

                mother = ""
                father = ""

                # Parents
                if len(_mother) > 0:
                    mother = self.__get_person(_mother)
                if len(_father) > 0:
                    father = self.__get_person(_father)

                birth_place = self.__get_place(birthplace, ())
                family_names = family
                family_group_label = family_names
                birth = Birth(
                    self._graph,
                    born_person,
                    birth_place,
                    date,
                    (),
                    (),
                    family_names,
                    (),
                    (),
                    mother,
                    father,
                )
                self.__insert_di_act(
                    birth,
                    (),
                    "Stephan Makowski",
                    "ProDomo",
                    "https://prodomo.icar-us.eu/aspect/" + id,
                    self._d1,
                )
                logging.debug(
                    "Added 'birth' for person '{}'".format(birth.main_person.label)
                )

    logging.info("Parsed the births")

    def add_burial(self, singleperson, burialday, burialplace, ids):
        """
        Add all burial events for the person
        """
        buried_person = self.__get_person(singleperson.Name)
        if not buried_person:
            return

        if burialday or burialplace:
            burialID = ids["Begraebnis"]
            burial_place = self.__get_place(burialplace, ())
            burial_ev = Burial(self._graph, buried_person, burial_place, burialday)
            burial = Aspect(self._graph, "Burial", Nampi_type.Mona.burial)

            burial_ev.add_relationship(Nampi_type.Core.adds_aspect, burial)

            self.__insert_di_act(
                burial_ev,
                (),
                "Stephan Makowski",
                "ProDomo",
                "https://prodomo.icar-us.eu/aspect/" + burialID,
                self._d1,
            )
        logging.info("Parsed the burials")

    def add_deaths(self, singleperson, deathday, deathplace, ids):
        """
        Add all death events from the deaths table.
        """

        died_person = self.__get_person(singleperson.Name)
        if not died_person:
            return
        if len(deathday) != 0:
            death_place = self.__get_place(deathplace, ())
            death = Death(self._graph, died_person, death_place, (), deathday, ())

            self.__insert_di_act(
                death,
                (),
                "Stephan Makowski",
                "ProDomo",
                "https://prodomo.icar-us.eu/aspect/" + ids["Tod"],
                self._d1,
            )
        logging.info("Parsed the deaths")

    def add_other_events(
        self,
        person: Person,
        label: str,
        date: str,
        semantics: Optional[str],
        reference: Optional[str],
        aspect: Optional[str],
        aspectkey: Optional[str],
        occupationkey: Optional[str],
        aspectlabel,
        name: Optional[str],
        participant: Optional[str],
        id: Optional[str],
        place: Optional[str]
    ):
        # get Event label from dict
        Monastery = None

        if semantics in Entities_dict and Entities_dict[semantics] is not None:
            Monastery = Entities_dict[semantics]
        elif reference in Entities_dict and Entities_dict[reference] is not None:
            Monastery = Entities_dict[reference]
        else:
            Monastery = ""

        if not person:
            # Only use entries with source
            logging.warning("No source entry for 'person' ")
            return

        Person = self.__get_person(person.Name)

        strPlace = ""
        Place = ""
        
        if hasattr(Monastery, "Place_Label"):
            strPlace = Monastery.Place_Label
            Place = self.__get_place(strPlace, Monastery.GeoId)
        elif place:
            Place = self.__get_place(place, "")
        # get various type by key from dict
        # leave if not present; core:aspect will be set automatically
        types = []
        try:
            if len(str(aspectkey)) > 0:
                types.append(_status_types[aspectkey])

            if len(occupationkey) > 0:
                types.append(_occupation_types[occupationkey])

        except:
            logging.info("Key not in Dict")

        varAspect =""
        alabel = ""

        if(aspectlabel.find("[Orden]") > -1):
            alabel = aspectlabel.replace("[Orden]", Monastery.AspectPart)
        else:
            alabel = aspectlabel

        varAspect = Aspect(self._graph,alabel, types)

        # check date
        # if it contains 4 digits, make earliest and latest date

        dateearly = ""
        datelast = ""
        if date:
            if len(date) == 4:
                dateearly = date + "-01-01"
                datelast = date + "-12-31"
                date = None

            elif len(date) == 7:
                dateearly = date + "-01"
                datelast = date + "-30"
                date = None

        if date:
            PlainEvent = Event(
                self._graph,
                Person,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                Place,
                date,
            )
        elif len(dateearly) > 0:
             PlainEvent = Event(
                self._graph,
                Person,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                Place,
                "",
                dateearly,
                datelast
            )     
        else: 
             PlainEvent = Event(
                self._graph,
                Person,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                Place,
            )                       


        if type(Monastery) is Entity_Importer:
            Kloster = self.__get_group(
                Monastery.Class, Monastery.Label, Monastery.Part_Of_Label
            )
            PlainEvent.add_relationship(
                Nampi_type.Core.changes_aspect_related_to, Kloster
            )


        PlainEvent.add_relationship(Nampi_type.Core.adds_aspect, varAspect)


        self.__insert_di_act(
            PlainEvent,
            (),
            "Stephan Makowski",
            "ProDomo",
            "https://prodomo.icar-us.eu/aspect/" + id,
            self._d1,
        )

    def add_investiture_events(self, person, invest_date):
        # get Event label from dict
        # print(invest_date.SemanticStm)
        # print(Entities_dict.keys())
        if (
            invest_date.SemanticStm in Entities_dict
            and Entities_dict[invest_date.SemanticStm] is not None
        ):
            Monastery = Entities_dict[invest_date.SemanticStm]
        elif (
            invest_date.Reference in Entities_dict
            and Entities_dict[invest_date.Reference] is not None
        ):
            Monastery = Entities_dict[invest_date.Reference]
        else:
            Monastery = ""

        strPlace = ""

        if hasattr(Monastery, "Place_Label"):
            strPlace = Monastery.Place_Label
            Place = self.__get_place(strPlace, Monastery.GeoId)

        Person = self.__get_person(person.Name)

        Religious_Name = Appellation(
            self._graph, person.Forename, Appellation_type.RELIGIOUS_NAME
        )

        Novice = Aspect(
            self._graph, "Novice", Nampi_type.Mona.member_of_a_religious_community
        )

        investiture = Event(
            self._graph,
            Person,
            Nampi_type.Core.has_main_participant,
            "Investiture in " + Monastery.Event,
            Nampi_type.Core.event,
            Place,
            invest_date.When,
        )

        if type(Monastery) is Entity_Importer:
            Kloster = self.__get_group(
                Monastery.Class, Monastery.Label, Monastery.Part_Of_Label
            )
            investiture.add_relationship(
                Nampi_type.Core.changes_aspect_related_to, Kloster
            )

        investiture.add_relationship(Nampi_type.Core.adds_aspect, Religious_Name.node)
        investiture.add_relationship(Nampi_type.Core.adds_aspect, Novice)

        # investiture.add_relationship(Nampi_type.Core.changes_aspect_related_to, Group)
        self.__insert_di_act(
            investiture,
            (),
            "Stephan Makowski",
            "ProDomo",
            "https://prodomo.icar-us.eu/aspect/" + invest_date.Id,
            self._d1,
        )

    def add_persons(self, persondata, birthdate="", birthplace="", ids=""):
        """
        Add all persons from the persons table not being added in birth events.
        """

        if not persondata:
            # Only use entries with source
            logging.warning("No source entry for 'person' ")
            return

        person_label = persondata.Name  # persondata.Forename + " " + persondata.Surname

        person = self.__get_person(persondata.Name)
        print("Person in Progress...{}")
        if person:

            # if not has_birth_event:
            #     # Get all family name variants from the person table
            family_names = persondata.Surname
            #                     safe_str(row, Column.family_name_gender_neutral), safe_str(row, Column.family_name)]
            #     # Get the official family name by looking through the ordered family_names list and picking the first match
            family_group_name = next((s for s in family_names if s), None)
            # Add family name group membership

            family = Family(self._graph, persondata.Surname)
            aspect = Aspect(self._graph, family_member_label)

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
                    "Stephan Makowski",
                    "ProDomo",
                    "https://prodomo.icar-us.eu/person/" + persondata.Id,
                    self._d1,
                )

            if len(persondata.Mother) != 0:
                mother = self.__get_person(persondata.Mother)
                become_member_event_mother = Event(
                    self._graph,
                    mother,
                    Nampi_type.Core.has_main_participant,
                    label="Become family member",
                )
                become_member_event_mother.add_relationship(
                    Nampi_type.Core.adds_aspect, aspect
                )
                become_member_event_mother.add_relationship(
                    Nampi_type.Core.changes_aspect_related_to, family
                )

                self.__insert_di_act(
                    become_member_event_mother,
                    (),
                    "Stephan Makowski",
                    "ProDomo",
                    "https://prodomo.icar-us.eu/aspekt/" + ids["Mutter"],
                    self._d1,
                )

            if len(persondata.Father) != 0:
                father = self.__get_person(persondata.Father)
                become_member_event_father = Event(
                    self._graph,
                    father,
                    Nampi_type.Core.has_main_participant,
                    label="Become family member",
                )
                become_member_event_father.add_relationship(
                    Nampi_type.Core.adds_aspect, aspect
                )
                become_member_event_father.add_relationship(
                    Nampi_type.Core.changes_aspect_related_to, family
                )

                self.__insert_di_act(
                    become_member_event_father,
                    (),
                    "Stephan Makowski",
                    "ProDomo",
                    "https://prodomo.icar-us.eu/aspekt/" + ids["Vater"],
                    self._d1,
                )

                # Add names for persons that don't have birth events
                # if family_names:
                # Add personal family name
                fn_assignment = Appellation_assignment(
                    self._graph,
                    person,
                    family_names,
                    Appellation_type.FAMILY_NAME,
                )
                self.__insert_di_act(
                    fn_assignment,
                    (),
                    "Stephan Makowski",
                    "ProDomo",
                    "https://prodomo.icar-us.eu/person/" + persondata.Id,
                    self._d1,
                )

            if birthdate:
                self.__add_births(
                    birthdate,
                    person_label,
                    family_names,
                    birthplace,
                    persondata.Id,
                    persondata.Mother,
                    persondata.Father,
                )

        logging.info("Parsed the persons")

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

    def __get_person(self, person_label: Optional[str]) -> Optional[Person]:

        gnd_id = ""
        gender = ""
        # )
        return Person.optional(self._graph, person_label, gender=gender, gnd_id=gnd_id)

    def __get_place(
        self, place_label: Optional[str], geoid: Optional[str]
    ) -> Optional[Place]:
        if geoid:
            geoname_id = geoid
        else:
            geoname_id = ""

        #  wikidata_id = self.__sheet.get_from_table(
        #     Table.PLACES, Column.name, place_label, Column.wikidata
        # )
        return Place.optional(self._graph, place_label, geoname_id, "")

    def __get_source_location(
        self, source_label: str, location_text: str
    ) -> Source_location:
        source_type_text = "Online Resource"
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
        interpretation_date_text: Optional[str] = None,
    ):
        author_label = author_label
        source_label = source_label
        source_location_label = source_location_label

        author = Author(self._graph, author_label)
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

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
import calendar
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
    "Abbas Lateranensis": Nampi_type.Mona.community_superior,
    "Abbess": Nampi_type.Mona.community_superior,
    "Abbot": Nampi_type.Mona.community_superior,
    "Academy professor": Nampi_type.Mona.educator,
    "Archbishop": Nampi_type.Mona.clergy,
    "Archdeacon": Nampi_type.Mona.clergy,
    "Archpriest": Nampi_type.Mona.clergy,
    "assessor": Nampi_type.Core.status,
    "Assistant emeritus of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Assistant of the Vicar of Bohemia": Nampi_type.Mona.office,
    "Augustinian father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Augustinian friar": Nampi_type.Mona.member_of_a_religious_community,
    "Augustinian prior": Nampi_type.Mona.community_superior,
    "Augustinian prior perpetuus": Nampi_type.Mona.community_superior,
    "Barnabite father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Barnabite friar": Nampi_type.Mona.member_of_a_religious_community,
    "Barnabite father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Benedictine father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Benedictine prior": Nampi_type.Mona.vice_community_superior,
    "Beneficiatus": Nampi_type.Mona.clergy,
    "Bibliothecarius": Nampi_type.Mona.office,
    "Bishop": Nampi_type.Mona.clergy,
    "Bishop elect": Nampi_type.Mona.clergy,
    "Camerarius": Nampi_type.Mona.monastic_office,
    "Canon": Nampi_type.Mona.clergy,
    "Canon regular": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Canoness regular": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Canonicus regius": Nampi_type.Mona.clergy,
    "Cantor": Nampi_type.Mona.monastic_office,
    "Capitularis": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Capuchine father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Capuchine friar": Nampi_type.Mona.member_of_a_religious_community,
    "Carmelite father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Carmelite nun": Nampi_type.Mona.member_of_a_religious_community,
    "Carmelite prioress": Nampi_type.Mona.community_superior,
    "Carthusian converse": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Carthusian convisitator": Nampi_type.Mona.visitator,
    "Carthusian hospes": Nampi_type.Mona.member_of_a_religious_community_visiting,
    "Carthusian prior": Nampi_type.Mona.community_superior,
    "Carthusian procurator": Nampi_type.Mona.vice_community_superior,
    "Carthusian subsacristan": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Carthusian vicar": Nampi_type.Mona.vice_community_superior,
    "Carthusian visitator": Nampi_type.Mona.visitator,
    "Cellarer": Nampi_type.Mona.monastic_office_with_manual_focus,
    "Chancellor": Nampi_type.Mona.office,
    "Chaplain": Nampi_type.Mona.clergy,
    "Choir monk": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Choir nun": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Cistercian father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Cistercian prior": Nampi_type.Mona.vice_community_superior,
    "Cistercian prioress": Nampi_type.Mona.community_superior,
    "Cistercian prioress emerita": Nampi_type.Mona.community_superior,
    "Cistercian subprior": Nampi_type.Mona.vice_community_superior,
    "Cistercian subprior emeritus": Nampi_type.Mona.vice_community_superior,
    "Cistercian subprioress": Nampi_type.Mona.vice_community_superior,
    "Cistercian vicar general": Nampi_type.Mona.community_superior,
    "Cistercian vicar general emeritus": Nampi_type.Mona.community_superior,
    "Cistercian visitator": Nampi_type.Mona.visitator,
    "Cleric": Nampi_type.Mona.clergy,
    "Coadiutor": Nampi_type.Core.status,
    "Commissioner general": Nampi_type.Core.status,
    "Concionator": Nampi_type.Mona.clergy,
    "Concionator jubilatus": Nampi_type.Mona.clergy,
    "Confessor": Nampi_type.Mona.clergy,
    "Consistorialis": Nampi_type.Core.status,
    "Consistorial councillor": Nampi_type.Mona.office_in_a_diocese,
    "converse": Nampi_type.Core.status,
    "Conversus": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Councillor": Nampi_type.Core.status,
    "Count palatine": Nampi_type.Mona.secular_office,
    "Court chaplain": Nampi_type.Mona.clergy,
    "Curatus": Nampi_type.Mona.clergy,
    "Curatus ecclesiasticus": Nampi_type.Mona.clergy,
    "Custos": Nampi_type.Mona.office,
    "Deacon": Nampi_type.Mona.clergy,
    "Dean": Nampi_type.Mona.community_superior,
    "Dean emeritus": Nampi_type.Mona.community_superior,
    "Decanissa": Nampi_type.Mona.community_superior,
    "Decanus foraneus": Nampi_type.Mona.community_superior,
    "Definitor": Nampi_type.Mona.community_superior,
    "Definitor of the German order province ": Nampi_type.Mona.community_superior,
    "Deputy of the estates of Carinthia": Nampi_type.Mona.secular_office,
    "Deputy of the estates of Lower Austria": Nampi_type.Mona.secular_office,
    "Deputy of the estates of Lower Austria emeritus": Nampi_type.Mona.secular_office,
    "Director of the bursary": Nampi_type.Mona.office,
    "Doctor of Laws": Nampi_type.Mona.academic_degree,
    "Doctor of Theology": Nampi_type.Mona.academic_degree,
    "Dominican administrator": Nampi_type.Mona.community_superior,
    "Dominican confessor": Nampi_type.Mona.clergy,
    "Dominican father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Dominican friar": Nampi_type.Mona.member_of_a_religious_community,
    "Dominican novice": Nampi_type.Mona.member_of_a_religious_community,
    "Dominican novice mistress": Nampi_type.Mona.professed_member_of_a_religious_community,
    "Dominican prior ": Nampi_type.Mona.community_superior,
    "Dominican prior provincialis": Nampi_type.Mona.community_superior,
    "Dominican prioress": Nampi_type.Mona.community_superior,
    "Dominican prioress emerita": Nampi_type.Mona.community_superior,
    "Dominican provincial vicar": Nampi_type.Mona.community_superior,
    "Dominican subprioress": Nampi_type.Mona.vice_community_superior,
    "Dominican vicar": Nampi_type.Mona.community_superior,
    "Donatus": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Fleischkuchlmeister": Nampi_type.Mona.monastic_office_with_manual_focus,
    "Franciscan Hermit friar": Nampi_type.Mona.member_of_a_religious_community,
    "Franciscan father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Franciscan friar": Nampi_type.Mona.member_of_a_religious_community,
    "friar": Nampi_type.Mona.member_of_a_religious_community,
    "Guardianus": Nampi_type.Mona.community_superior,
    "Guest": Nampi_type.Mona.member_of_a_religious_community_visiting,
    "Guest master": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Hermit": Nampi_type.Mona.religious_life_outside_a_community,
    "Imperial administrator": Nampi_type.Mona.community_superior,
    "Imperial and royal councillor": Nampi_type.Mona.secular_office,
    "Imperial and royal secret councillor": Nampi_type.Mona.secular_office,
    "Imperial chamberlain": Nampi_type.Mona.secular_office,
    "Imperial councillor": Nampi_type.Mona.secular_office,
    "Imperial court chaplain": Nampi_type.Mona.clergy,
    "Imperial parish priest": Nampi_type.Mona.clergy,
    "Imperial secret councillor": Nampi_type.Mona.secular_office,
    "Jesuit brother": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Jesuit father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Jesuit priest": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Judge": Nampi_type.Mona.secular_office,
    "Kitchen master": Nampi_type.Mona.monastic_office_with_manual_focus,
    "Laica": Nampi_type.Core.status,
    "Laicus": Nampi_type.Core.status,
    "Lay brother": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Lay sister": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Lector": Nampi_type.Mona.office,
    "Lector theologiae": Nampi_type.Mona.educator,
    "Magnus Conestabilis": Nampi_type.Mona.secular_office,
    "Marshal of Tyrolia": Nampi_type.Mona.secular_office,
    "Master of theology": Nampi_type.Mona.academic_degree,
    "Member": Nampi_type.Mona.member_of_a_religious_community,
    "Minister of ceremonies": Nampi_type.Mona.office_in_a_diocese,
    "Minorite father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Minorite friar": Nampi_type.Mona.member_of_a_religious_community,
    "Missionarius apostolicus": Nampi_type.Mona.office,
    "Novice": Nampi_type.Mona.member_of_a_religious_community,
    "Novice master": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Novice master emeritus": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Novice mistress": Nampi_type.Mona.vice_community_superior,
    "nun": Nampi_type.Core.status,
    "Oblatus": Nampi_type.Mona.member_of_a_religious_community_with_manual_focus,
    "Observant definitor": Nampi_type.Mona.community_superior,
    "Observant father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Observant friar": Nampi_type.Mona.member_of_a_religious_community,
    "Observant lector generalis": Nampi_type.Core.status,
    "Oeconomus": Nampi_type.Mona.office,
    "Official": Nampi_type.Mona.office_in_a_diocese,
    "Official in Kirchberg": Nampi_type.Mona.office_in_a_diocese,
    "order prefect of the mission": Nampi_type.Core.status,
    "order prefect of the Mission in Carinthia, Krain and Styria": Nampi_type.Core.status,
    "Parish priest": Nampi_type.Mona.clergy,
    "Parochus emeritus": Nampi_type.Mona.clergy,
    "Parson": Nampi_type.Mona.clergy,
    "Pater immediatus for Carinthia, Krain and parts of Austria": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Pauline father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Pauline friar": Nampi_type.Mona.member_of_a_religious_community,
    "Pilgrim": Nampi_type.Mona.religious_life_outside_a_community,
    "Poenitentiarius": Nampi_type.Mona.clergy,
    "Poenitentiarius apostolicus": Nampi_type.Mona.clergy,
    "Poor Clare nun": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Praedicator generalis": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Praefectus": Nampi_type.Core.status,
    "Praefectus aulae": Nampi_type.Mona.monastic_office,
    "Praefectus aulae et judiciorum": Nampi_type.Mona.office,
    "Praefectus rationum": Nampi_type.Mona.office,
    "Praefectus sylvarum": Nampi_type.Mona.office,
    "Praepositus of the Congregation of the Austrian Lateran Canons regular": Nampi_type.Mona.community_superior,
    "Praesentatus theologiae": Nampi_type.Core.status,
    "Praeses of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Praeses of the Josephsbruderschaft emeritus": Nampi_type.Mona.office,
    "Praeses of the prelates of Lower Austria in the diet": Nampi_type.Mona.office,
    "Praeses of the Rosenkranzbruderschaft": Nampi_type.Mona.office,
    "praetor": Nampi_type.Core.status,
    "Prefect": Nampi_type.Core.status,
    "Prefect of the mission": Nampi_type.Core.status,
    "Prelate": Nampi_type.Mona.community_superior,
    "Premonstratensian father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Presbyter jubilatus": Nampi_type.Mona.clergy,
    "President of the congregation": Nampi_type.Core.status,
    "Priest": Nampi_type.Mona.clergy,
    "Priest monk": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Prior emeritus": Nampi_type.Mona.community_superior,
    "Prior perpetuus": Nampi_type.Mona.community_superior,
    "Prioress": Nampi_type.Mona.community_superior,
    "Prioress emerita": Nampi_type.Mona.community_superior,
    "Prioress of the Poor Clares": Nampi_type.Mona.community_superior,
    "Procurator": Nampi_type.Mona.monastic_office,
    "Professa jubilata": Nampi_type.Mona.professed_member_of_a_religious_community,
    "Professus jubilatus": Nampi_type.Mona.professed_member_of_a_religious_community,
    "Promotor of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Protonotary apostolic": Nampi_type.Mona.clergy,
    "Provincialis emeritus": Nampi_type.Mona.community_superior,
    "Provost": Nampi_type.Mona.community_superior,
    "rector": Nampi_type.Core.status,
    "Rector of the Jesuit college": Nampi_type.Mona.ruler_of_a_school,
    "Rector of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Rector of the Josephsbruderschaft emeritus": Nampi_type.Mona.office,
    "Rector of the University of Salzburg": Nampi_type.Mona.ruler_of_a_school,
    "Rector of the University of Vienna": Nampi_type.Mona.ruler_of_a_school,
    "Regens chori": Nampi_type.Mona.monastic_office_with_spiritual_focus,
    "Royal vicar": Nampi_type.Core.status,
    "Sacerdos jubilatus": Nampi_type.Mona.clergy,
    "Sacrista": Nampi_type.Mona.monastic_office,
    "Sacristan": Nampi_type.Mona.monastic_office,
    "Second assistant of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Secretary": Nampi_type.Mona.office,
    "Secretrary emeritus": Nampi_type.Mona.office,
    "Secretary emeritus of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Secretary of the Imperial secret counsel in Lower Austria": Nampi_type.Mona.secular_office,
    "Secretary of the Josephsbruderschaft": Nampi_type.Mona.office,
    "Secret councillor": Nampi_type.Mona.office,
    "Secular priest": Nampi_type.Mona.clergy,
    "Senior": Nampi_type.Mona.member_of_a_religious_community,
    "Senior capitularis": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Senior jubilatus": Nampi_type.Mona.member_of_a_religious_community,
    "Servite father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Servite friar": Nampi_type.Mona.member_of_a_religious_community,
    "Servite nun": Nampi_type.Mona.member_of_a_religious_community,
    "Steward for the hereditary lands": Nampi_type.Core.status,
    "Subprior": Nampi_type.Mona.vice_community_superior,
    "Subprior emeritus": Nampi_type.Mona.vice_community_superior,
    "Subprioress": Nampi_type.Mona.vice_community_superior,
    "Suffragan bishop": Nampi_type.Mona.clergy,
    "Superior": Nampi_type.Mona.community_superior,
    "Superioress": Nampi_type.Mona.community_superior,
    "Theatine father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Thesaurarius": Nampi_type.Mona.monastic_office,
    "Titular abbot": Nampi_type.Mona.community_superior,
    "Titular bishop": Nampi_type.Mona.clergy,
    "University professor": Nampi_type.Mona.educator,
    "university rector": Nampi_type.Core.status,
    "Ursuline nun": Nampi_type.Mona.member_of_a_religious_community,
    "Velata professa": Nampi_type.Mona.member_of_a_religious_community,
    "Vicar": Nampi_type.Mona.clergy,
    "Vicar general": Nampi_type.Mona.office_in_a_diocese,
    "Vicar general of the Cistercian order": Nampi_type.Mona.community_superior,
    "Vicar senior": Nampi_type.Core.status,
    "Vicerector of the Josephsbruderschaft": Nampi_type.Core.status,
    "Vicerector of the Josephsbruderschaft emeritus": Nampi_type.Core.status,
    "Vicedean": Nampi_type.Mona.vice_community_superior,
    "Visitator": Nampi_type.Mona.visitator,
    "Visitator for Hungary, Styria, Upper and Lower Austria": Nampi_type.Mona.visitator,
    "Dominican / Premonstratensian father": Nampi_type.Mona.member_of_a_religious_community_with_spiritual_focus,
    "Profess": Nampi_type.Core.status,
    "Unspecified aspect": Nampi_type.Mona.unspecified_aspect
}

_occupation_types = {
    "Administration of a community": Nampi_type.Mona.administration_of_a_community,
    "Associated parish clergy": Nampi_type.Mona.associated_parish_clergy,
    "Clergy": Nampi_type.Mona.clergy,
    "Official": Nampi_type.Mona.official,

    "Rule of a community": Nampi_type.Mona.rule_of_a_community,
}

authors = [
    "Stephan Makowski",
    "Irene Rabl",
    "Patrick Fiska"
]

def safe_str(row: Series, column: str) -> Optional[str]:
    return str(row[column]) if column in row else None


Entities_dict = {}


class Nampi_data_entry_form_parser_prodomo:
    """A parser that parses the NAMPI input tables and transforms the data to an RDF graph."""

    _graph: Nampi_graph

    # Get all Entries from Group_Entities Spreadsheet
    def getEntities(self):


        # Extract and print all of the values
        list_of_hashes = GetTypesAndStati("Group Entities").getData()
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
                    authors,
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
                authors,
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
                authors,
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
        place: Optional[str],
        datefrom: Optional[str],
        dateto:Optional[str]
    ):
        # get Event label from dict
        Monastery = None
        Kloster = None

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

        objPerson = self.__get_person(person.Name)

        strPlace = ""
        objPlace = ""
        place = ""

        if hasattr(Monastery, "Place_Label"):
            strPlace = Monastery.Place_Label
            objPlace = self.__get_place(strPlace, Monastery.GeoId)
        elif place:
            objPlace = self.__get_place(place, "")

 

        # check date
        # if it contains 4 digits, make earliest and latest date

        dateearly = ""
        datelast = ""
        datetokens = ""
        if date:
            if len(date) == 4:
                dateearly = date + "-01-01"
                datelast = date + "-12-31"
                date = None

            elif len(date) == 7:
                datetokens = date.split("-")
                dateearly = date + "-01"
                datelast = date + "-" + str(calendar.monthrange(int(datetokens[0]),int(datetokens[1]))[1])
                date = None

        if datefrom:
            if(len(datefrom))== 4:
                dateearly = datefrom + "-01-01"
            elif(len(datefrom))==7:
                dateearly = datefrom + "-01"
            else:
                dateearly = datefrom

        if dateto:        
            
            if(len(dateto.strip()))== 4:
                datelast = dateto + "-12-31"
            elif(len(dateto.strip()))==7:
                datetokens = dateto.split("-")
                datelast = dateto + "-" + str(calendar.monthrange(int(datetokens[0]),int(datetokens[1]))[1])
            else:
                datelast = dateto   

        if dateearly == "0000-00-00":
            dateearly = ""

        if datelast == "0000-00-00":
            datelast = ""

        if dateearly.find("0000") > -1:
            dateearly = ""

        if datelast.find("0000") > -1:
            datelast = ""

        if len(dateearly) > 0  :
             PlainEvent = Event(
                self._graph,
                objPerson,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                objPlace,
                "",
                dateearly,
                datelast
            )
        elif date:
            PlainEvent = Event(
                self._graph,
                objPerson,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                objPlace,
                date,
            )     
        else: 
             PlainEvent = Event(
                self._graph,
                objPerson,
                Nampi_type.Core.has_main_participant,
                label,
                Nampi_type.Core.event,
                objPlace,
            )                       


        if type(Monastery) is Entity_Importer:
            Kloster = self.__get_group(
                Monastery.Class, Monastery.Label, Monastery.Part_Of_Label
            )
            PlainEvent.add_relationship(
                Nampi_type.Core.changes_aspect_related_to, Kloster
            )


       # get various type by key from dict
        # leave if not present; core:aspect will be set automatically
        types = []
        try:
            if len(str(aspectkey)) > 0:
                types.append(_status_types[aspectkey])

            if len(occupationkey) > 0:
                types.append(_occupation_types[occupationkey])

            if len(types) == 0:
                types.append(_status_types["Unspecified aspect"])

        except:
            logging.info("Key not in Dict")
       
        varAspect =""
        alabel = ""

        if aspectlabel is not None:  
            if(aspectlabel.find("[Orden]") > -1 and hasattr(Monastery, "AspectPart")):
                alabel = aspectlabel.replace("[Orden]", Monastery.AspectPart)
            else:  
                alabel = aspectlabel


        if alabel is not None and len(alabel.strip()) > 0:

            varAspect = Aspect(self._graph,alabel.capitalize(), types)
            
            PlainEvent.add_relationship(Nampi_type.Core.adds_aspect, varAspect)


            self.__insert_di_act(
                PlainEvent,
                (),
                authors,
                "ProDomo",
                "https://prodomo.icar-us.eu/aspect/" + id,
                self._d1,
            )

    def add_investiture_events(self, person, invest_dates):
        # get Event label from dict
        # print(invest_date.SemanticStm)
        # print(Entities_dict.keys())
        if not isinstance(invest_dates, list):
                # If type is not list then make it list
                invest_dates = [invest_dates]

        for invest_date in invest_dates:
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
                objPlace = self.__get_place(strPlace, Monastery.GeoId)

            objPerson = self.__get_person(person.Name)

            Religious_Name = Appellation(
                self._graph, person.Forename, Appellation_type.RELIGIOUS_NAME
            )

            Novice = Aspect(
                self._graph, "Novice", Nampi_type.Mona.member_of_a_religious_community
            )

            investiture = Event(
                self._graph,
                objPerson,
                Nampi_type.Core.has_main_participant,
                "Investiture in " + Monastery.Event,
                Nampi_type.Core.event,
                objPlace,
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
                authors,
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
                    authors,
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
                    authors,
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
                    authors,
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
                    authors,
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
                    ids["Geburt"],
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
        authors: str = "",
        source_label: str = "",
        source_location_label: str = "",
        interpretation_date_text: Optional[str] = None,
    ):
        author_label = authors
        source_label = source_label
        source_location_label = source_location_label

        author =authors #Author(self._graph, author_label)
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

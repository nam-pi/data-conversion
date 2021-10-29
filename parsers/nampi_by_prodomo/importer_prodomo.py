# -*- coding: utf-8 -*-
import logging
import glob
from operator import contains
import sys
import os
import requests
from modules.date import Date
import xmltodict
import json
import gspread
import traceback

from lxml import etree
from types import SimpleNamespace
from collections import OrderedDict
from requests.api import get
from oauth2client.service_account import ServiceAccountCredentials

from modules.nampi_graph import Nampi_graph
from parsers.nampi_by_prodomo.classes.place import Place
from parsers.nampi_by_prodomo.classes.person import Person
from parsers.nampi_by_prodomo.classes.date import Dates
from parsers.nampi_by_prodomo.classes.placename import PlaceName
from parsers.nampi_by_prodomo.classes.time import Time
from parsers.nampi_by_prodomo.classes.events import ExternalEvent
from parsers.nampi_by_prodomo.nampi_data_entry_form_prodomo import (
    Nampi_data_entry_form_parser_prodomo,
)

# prepare dicts
ns = dict(
    aodl="http://pdr.bbaw.de/namespaces/aodl/",
    exist="http://exist.sourceforge.net/NS/exist",
    mods="http://www.loc.gov/mods/v3",
    podl="http://pdr.bbaw.de/namespaces/podl/",
)

selector = dict(
    persName="surname forename",
    time="",
    placeName="",
    date="",
    spatialStm="",
    place="",
    timeStm="",
    semanticStm="",
)

types = dict(
    Geburt="",
    Abt="",
    Beziehung="",
    Bischof="",
    Geschwister="",
    Konvent="",
    Pfarrvikar="",
    Priester="",
    Subdiakon="",
    Taufe="",
    Tod="",
)

subtypes = dict(
    Einkleidung="", forename="", Primiz="", Profess="", surname="", Vorname=""
)

Entities_dict = {}
Event_dict = {}
TypSub = {}


class Importer_prodomo:
    _graph: Nampi_graph
    _persName: None
    prodomo_parser: None
    def getEvents(self):
         # use creds to create a client to interact with the Google Drive API
        # scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(".credentials.json")
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        sheet = client.open("Events").sheet1

        # Extract and print all of the values
        list_of_hashes = sheet.get_all_records()
        i = 0
        print("--Start analyzing Event-Spreadsheet --")
        for i in list_of_hashes:
            eEvent = ExternalEvent()
            key = i["TypSubtyp"].strip()
            eEvent.Key = key
            eEvent.Label = i["rdfs:label"]
            eEvent.Date =  i["Datum - aodl:date"]
            eEvent.Group = i["Gruppe"]
            eEvent.Place = i["core:takes_place_at"]
            eEvent.Relation = i["aspekt-relationship"]
            eEvent.Occupationkey = i["OccupationKey"]
            eEvent.Aspectkey = i["Aspektkey"]
            eEvent.Type = i["Aspekttyp"]
            eEvent.Aspectlabel = i["Aspektlabel"]
            eEvent.Participant = i["core:has_participant"]
            eEvent.Semantic = i["semantic"]
            eEvent.Else = i["else"]

            if key not in Event_dict:
                Event_dict[key] = eEvent
            else:
                if not isinstance(Event_dict[key], list):
                    # If type is not list then make it list
                    Event_dict[key] = [Event_dict[key]]
                    
                Event_dict[key].append(eEvent)

        print("--Ready with Event-Spreadsheet --")

    # collect all TypSubtypes for iterative Workflow
    def addTypSub(self, kombi, item):
        if kombi not in Entities_dict:
            Entities_dict[kombi] = item
        else:
            if not isinstance(Entities_dict[kombi], list):
                # If type is not list then make it list
                Entities_dict[kombi] = [Entities_dict[kombi]]
                
            Entities_dict[kombi].append(item)

    def __init__(self, graph: Nampi_graph):
        self._graph = graph
        self.prodomo_parser = Nampi_data_entry_form_parser_prodomo(self._graph)
        print("init prodomo parser")
        # init variables and URLs
        baseURL = "https://prodomo.icar-us.eu/rest/db?_wrap=yes&_howmany=1000&_query="
        personQuery = "xquery version '3.1';declare namespace podl = 'http://pdr.bbaw.de/namespaces/podl/';declare namespace aodl = 'http://pdr.bbaw.de/namespaces/aodl/'; collection('/db/apps/prodomo/data/pdr/person')//podl:person/data(@id)"

        # Get all Persons and start querying
        url = baseURL + personQuery
        response = requests.get(url)
        dict_data = xmltodict.parse(response.content)

        # gather events from spreadsheet
        logging.info("Start prefetching events")
        self.getEvents()
        logging.info("Finished prefetching events")

        # iterate over persons
        for person in dict_data.get("exist:result").get("exist:value"):
            personID = str(person.get("#text"))

            # prepare query for aspects
            query = "xquery version '3.1'; declare namespace podl = 'http://pdr.bbaw.de/namespaces/podl/'; declare namespace aodl = 'http://pdr.bbaw.de/namespaces/aodl/'; import module namespace functx='http://www.functx.com' at 'xmldb:exist:///db/system/repo/functx-1.0.1/functx/functx.xq'; declare function local:addId($node) {     let $r1 := functx:add-attributes($node,xs:QName('id') ,data(root($node)//aodl:aspect/@id))    return         $r1     }; declare function local:addSemantic($node, $base) {     let $r1 := functx:add-attributes($node,xs:QName('semanticStm') ,root($base)//aodl:semanticStm/text() )     let $r2 := functx:add-attributes($r1,xs:QName('reference') ,root($base)//aodl:reference/text() )     return $r2     }; declare function local:addPlace($node, $base) {         let $r1 :=    if(exists(root($base)//aodl:spatialStm/aodl:place)) then             functx:add-attributes($node,xs:QName('placename') ,root($base)//aodl:spatialStm/aodl:place/text() )        else            $node    return $r1}; let $cols := collection('/db/apps/prodomo/data/pdr/aspect')//aodl:relation[data(@object)='" + personID + "'] return   for $col in $cols        let $root := root($col)//.[@type][@type != 'undefined']           let $base :=             for $item in $root                 let $ided := local:addId($item)              let $place := local:addPlace($ided, $item)                 return                     local:addSemantic($place, $item)  return   $base"
            url = baseURL + query
            response = requests.get(url)
            dict_data = xmltodict.parse(response.content)

            tagName = ""
            times = {}
            dates = {}
            places  = {}
            placenames = {}
            singlePerson = Person()
            ids  = {}
            parents  = {}
            print("Creating Person: " + personID)
            # iterate over result set
            for key in dict_data.get("exist:result").keys():

                # prepare Tag without Namespace
                tagName = ""
                if str(key).index(":") > 0:
                    arrKey = key.split(":")
                    tagName = arrKey[1]

                # check if Tag is allowed; if not, continue else do build strings
                if not tagName in selector:
                    continue
                else:

                    # PERSON
                    if tagName == "persName":

                        persName = dict_data.get("exist:result").get(key)
                        singlePerson = Person()
                        for entry in persName:
                            try:
                                typ = ""
                                subtyp = ""
                                singlePerson.Id = personID


                                typ = entry.get("@type")
                                subtyp = entry.get("@subtype")
                                text = entry.get("#text")

                                if typ == "surname":
                                    singlePerson.Surname = text
                                elif typ == "forename":
                                    singlePerson.Forename = text
                                elif typ == "Eltern" and subtyp == "Vater":
                                    ids["Vater"] = entry.get("@id")
                               
                                    singlePerson.Father = text
                                    parents[subtyp] = text
                                elif typ == "Eltern" and subtyp == "Mutter":
                                    
                                    ids["Mutter"] = entry.get("@id")
                                    singlePerson.Mother = text
                                    parents[subtyp] = text

                                if typ is not None and subtyp is not None:
                                    typsub = typ+subtyp
                                elif typ is not None:
                                    typsub = typ

                                self.addTypSub(typsub, singlePerson)
                            except:
                                print(traceback.format_exc())
                                singlePerson.Surname = "na"
                                singlePerson.Forename = "na"

                    # ASPEKT Date
                    elif tagName == "date":
                        date = dict_data.get("exist:result").get(key)
                        typsub = ""
                        for entry in date:
                            personDate = Dates()
                            personDate.persId = personID

                            try:
                                typ = entry.get("@type")
                                if entry.get("@subtype"):
                                    subtype = entry.get("@subtype")
                                else:
                                    subtype = ""
                                text = entry.get("#text")
                                when = entry.get("@when")
                                strid = entry.get("@id")
                                semanticStm = entry.get("@semanticStm")
                                placename = entry.get("@placename")
                                notafter = entry.get("@notAfter")
                                notbefore = entry.get("@notBefore")
                                to = entry.get("@to")

                                if len(when.strip()) == 0:
                                    continue
                                personDate.Id = strid
                                personDate.Text = text
                                personDate.Type = typ
                                personDate.Subtype = subtype
                                personDate.When = when
                                personDate.PlaceName = placename
                                personDate.SemanticStm = semanticStm


                                if entry.get("@reference"):
                                    personDate.Reference = entry.get("@reference")
                                else:
                                    personDate.Reference = ""

                                ids[typ] = id

                                typsub = typ+subtype

                                self.addTypSub(typsub, personDate)

                            except:
                                personDate.Text = "na"
                                typsub = ""
                            # print(personDate)
                            if typsub not in dates:
                                dates[typsub] = personDate

                            else:
                                if not isinstance(dates[typsub], list):
                                    # If type is not list then make it list
                                    dates[typsub] = [dates[typsub]]
                        
                                dates[typsub].append(personDate)


                    # ASPEKT place
                    elif tagName == "place":
                        place = dict_data.get("exist:result").get(key)

                        for entry in place:

                            if isinstance(entry, dict):

                                placeObject = Place()
                                placeObject.persId = personID
                                # print(entry)
                                typ = entry.get("@type")

                                if entry.get("@subtype"):
                                    subtype = entry.get("@subtype")
                                else:
                                    subtype = ""

                                if entry.get("@key"):
                                    key = entry.get("@key")
                                else:
                                    key = ""

                                text = entry.get("#text")
                                when = entry.get("@when")
                                id = entry.get("@id")
                                semanticstm = entry.get("@semanticStm")
                                placename = entry.get("@placename")

                                placeObject.Id = id
                                placeObject.Text = text
                                placeObject.Type = typ
                                placeObject.Key = key
                                placeObject.Subtype = subtype
                                placeObject.When = when
                                placeObject.SemanticStm = semanticstm
                                placeObject.PlaceName = placename


                                # print(placeObject)
                                if places.get(typ) is None:
                                    places[typ] = placeObject

                                typsub = typ+subtype
                                self.addTypSub(typsub, placeObject)

                    # ASPEKT placeName
                    elif tagName == "placename":
                        placename = dict_data.get("exist:result").get(key)

                        for entry in placename:
                            placenameObject = PlaceName()
                            placenameObject.persId = personID

                            typ = entry.get("@type")

                            if entry.get("@subtype"):
                                subtype = entry.get("@subtype")
                            else:
                                subtype = ""

                            if entry.get("@ana"):
                                ana = entry.get("@ana")
                            else:
                                ana = ""

                            if entry.get("@when"):
                                when = entry.get("@when")
                            else:
                                when = ""

                            id = entry.get("@id")
                            semanticstm = entry.get("@semanticStm")
                            placename = entry.get("@placename")

                            placenameObject.Id = id
                            placenameObject.Ana = ana
                            placenameObject.Type = typ
                            placenameObject.Subtype = subtype
                            placenameObject.When = when
                            placenameObject.SemanticStm = semanticstm
                            placenameObject.PlaceName = placename

                            # print(placenameObject)
                            if not placenames[typ]:
                                placenames[typ] = placenameObject

                            typsub = typ+subtype
                            self.addTypSub(typsub, placenameObject)

                    # ASPEKT Time
                    elif tagName == "time":
                        time = dict_data.get("exist:result").get(key)

                        for entry in time:
                            personTime = Time()
                            personTime.persId = personID

                            try:
                                typ = entry.get("@type")

                                if entry.get("@subtype"):
                                    subtype = entry.get("@subtype")
                                else:
                                    subtype = ""

                                text = entry.get("#text")
                                when = entry.get("@when")
                                id = entry.get("@id")
                                semanticstm = entry.get("@semanticStm")
                                placename = entry.get("@placename")

                                personTime.Id = id
                                personTime.Text = text
                                personTime.Type = typ
                                personTime.Subtype = subtype
                                personTime.When = when
                                personTime.SemanticStm = semanticstm
                                personTime.PlaceName = placename

                                typsub = typ+subtype
                                self.addTypSub(typsub, personTime)

                            except:
                                personTime.Text = "na"
                            # print(personTime)

                            times[typ] = personTime

            #
            # Create Person and add Birthday
            #
            birthdays = dates.get("Geburt")
            birthplace = places.get("Geburt")

            if type(birthdays) is list:
                for birthday in birthdays:

                    bday = self._buildDate(birthday)
                    print("GEBURTSTAG")
                    print(bday)
                    ids["Geburt"] = birthday.Id
                    break
                    
            elif type(birthdays) is Dates:
                    bday = self._buildDate(birthdays)
                    ids["Geburt"] = birthdays.Id
            else:
                bday = ""

            print("GEBURTSTAG")
            print(bday)

            if birthplace:
                bplace = birthplace._text
                ids["Geburtsort"] = birthplace.Id
            else:
                bplace = ""

            self.prodomo_parser.add_persons(singlePerson, bday, bplace, ids)

            #
            # Create Death
            #
            deaths = dates.get("Tod")
            deathlocations = places.get("Tod")

            if type(deaths) is list:
                for death in deaths:
                    deathday = self._buildDate(death)
                    ids["Tod"] = death.Id
                    print(death.Id)
                  
            elif type(deaths) is Dates:
                deathday = self._buildDate(deaths)
                ids["Tod"] = deaths.Id
            else:
                deathday = ""

            if type(deaths) is list:
                return

            if deathlocations:
                deathplace = deathlocations._text
                ids["TodesOrt"] = deathlocations.Id
            else:
                deathplace = ""
            #           print(personID)
            if deaths is not None:
                self.prodomo_parser.add_deaths(singlePerson, deathday, deathplace, ids)

            #
            # Create Burial
            #
            burial = dates.get("Begräbnis")
            buriallocations = places.get("Begräbnis")

            if burial:
                burialday = self._buildDate(burial)
                ids["Begraebnis"] = burial.Id

            else:
                burialday = ""

            if buriallocations:
                burialplace = buriallocations._text
                ids["Begraebnis"] = buriallocations.Id

            # print(personID)
            else:
                burialplace = ""
                
            self.prodomo_parser.add_burial(singlePerson, burialday, burialplace, ids)

            # Investitur
            if dates.get("KonventEinkleidung") is not None:
                #print(dates.get("KonventEinkleidung"))
                
                self.prodomo_parser.add_investiture_events( singlePerson, dates.get("KonventEinkleidung") )


            # Other Events
            for key in Entities_dict:
                
                # Check if Key exists 
                try:    
                    if Event_dict[key]:
                        # get origin data object
                        DataEntries = Entities_dict[key]

                        # get corresponding rule set
                        InfoEntry = Event_dict[key]

                        #print("Current Key: " + key)
                        
                        # Data = ""

                        if not(isinstance(DataEntries, list)):
                            
                            self.doChecker(DataEntries, InfoEntry, singlePerson)
                        else:
                            for DataEntry in DataEntries:

                                self.doChecker(DataEntry, InfoEntry, singlePerson)

                except Exception as e:
                    print(e)

            # Init Variablen
            tagName = ""
            times.clear()
            dates.clear()
            places.clear()
            placenames.clear()
            singlePerson = Person()
            ids.clear()
            parents.clear()
            Entities_dict.clear()
            dates.clear()
            

    def doChecker(self, DataEntry, InfoEntries, singlePerson):

        if not(isinstance(InfoEntries, list)):
            self.doCheckerRoutine(DataEntry, InfoEntries, singlePerson)
        else:
            for InfoEntry in InfoEntries:
                self.doCheckerRoutine(DataEntry, InfoEntry, singlePerson)
            

    def doCheckerRoutine(self, DataEntry, InfoEntry, singlePerson):
        
        
        # check if date
        if type(DataEntry) is Dates or type(DataEntry) is Place or type(DataEntry) is PlaceName:
                                    
            # init
            label = ""

            # Take informations from Date and try to catch the correct aspect
            arrDates = InfoEntry.Date.split(" ")

            try:
                if(len(arrDates) > 1):
                    for attribute in arrDates:
                        date = self.checkexistence(str(attribute), DataEntry)
                        #if date is not None:
                        #build event
                        label = self.buildStrings(DataEntry, InfoEntry)
                        self.createEvent(DataEntry, label, DataEntry.When, InfoEntry.Aspectkey, InfoEntry.Occupationkey, InfoEntry.Aspectlabel, InfoEntry.Participant, DataEntry.Id, singlePerson)
                        return
                else:
                    date = self.checkexistence(arrDates, DataEntry)
                    
                    #if date is not None:
                    label = self.buildStrings(DataEntry,InfoEntry)
                    self.createEvent(DataEntry, label, DataEntry.When,  InfoEntry.Aspectkey, InfoEntry.Occupationkey, InfoEntry.Aspectlabel, InfoEntry.Participant, DataEntry.Id, singlePerson)

            except:    
                print(traceback.format_exc())

            #print("Label gelabeld: " + label)


    def createEvent(self, DataEntry, label, date,  aspectKey, occupationKey, aspectLabel, participant, id, singlePerson) -> str:
        if len(label) > 0:
            semantics = ""
            reference = ""
            
            if type(DataEntry) is Dates:
                reference = DataEntry.Reference
                semantics = DataEntry.SemanticStm
            
            if type(DataEntry) is Place:
                semantics = DataEntry.PlaceName
            
            self.prodomo_parser.add_other_events(singlePerson, label, date, semantics, reference,"" ,aspectKey, occupationKey, aspectLabel, "", participant, id, DataEntry.PlaceName)

    def buildStrings(self, DataEntry, InfoEntry) -> str:
        # clear labeltext1
        label = ""
        if hasattr(InfoEntry, "Label"):
            label = InfoEntry.Label

        label = label.replace("[Klostername]", "")
        label = label.replace("[aodl:name]", "")
        label = label.replace("[aodl:placeName]", "")
        label = label.replace("[Pfarrname]", "")
        labelGroup = ""
        # getting Group / Monastery
        group = InfoEntry.Group

        if group:
            # get Group via content of variable group
            if(str(group).strip().upper() == "AODL:SEMANTICSTM"):
                # do something
                labelGroup = DataEntry.SemanticStm
            elif(str(group).strip().upper().find("AODL:PLACENAME") > -1 ):          
                labelGroup = DataEntry.PlaceName

            elif(type(DataEntry) is Date):
                labelGroup = DataEntry.Reference
            else:
                if type(DataEntry) is Date:
                    labelGroup = DataEntry.SemanticStm
                else:
                    labelGroup = DataEntry.PlaceName

        # just take some group
        if label:
            returnlabel = label.strip() 
        if labelGroup:
            returnlabel = returnlabel + " " + labelGroup

        return returnlabel



    # Check Rules and test, if DataEntry contains searched patterns
    def checkexistence(self, attribute, DataEntry) -> bool:
        Att = str(attribute).replace("@", "")

        if type(DataEntry) is Date:
            if  (Att.upper() == "FROM"):
                if len(DataEntry.From.strip()) > 1:
                    # apply event / aspect
                    logging.info("From was true ")
                    return DataEntry.From.strip()
            elif (Att.upper() == "TO"):
                if len(DataEntry.To.strip()) > 1:
                    # apply event / aspect
                    logging.info("To was true ")
                    return DataEntry.To.strip()
            elif (Att.upper() == "WHEN"):
                if len(DataEntry.When.strip()) > 1:
                    # apply event / aspect
                    logging.info("When was true ")
                    return DataEntry.When.strip()
            elif (Att.upper() == "NOTAFTER"):
                if len(DataEntry.NotAfter.strip()) > 1:
                    # apply event / aspect
                    logging.info("NotAfter was true ")
                    return DataEntry.NotAfter.strip()
            elif (Att.upper() == "NOTBEFORE"):
                if len(DataEntry.NotBefore.strip()) > 1:
                    # apply event / aspect
                    logging.info("NotBefore was true ")
                    return DataEntry.NotBefore.strip()

        else:
            return None
            
    # Prepare Date
    def _buildDate(self, date):

        try:
            if len(date._notAfter.split("-")) == 3:
                returndate = date._notAfter
            elif len(date._notAfter.split("-")) == 2:
                returndate = date._notAfter + "-30"
            else:
                returndate = ""
        except:
            returndate = ""
        return returndate

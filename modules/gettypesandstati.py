from typing import Dict, Optional, Type

import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials


class GetTypesAndStati:
    """An abstraction layer that provides data from tables in Google sheets."""

    _data: Dict
    _value: {}

    def __init__(self, sheet_name: Optional[str]):

        sheet_data = ""
        # use creds to create a client to interact with the Google Drive API
        # scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(".credentials.json")
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        if sheet_name == "Statuses":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Statuses")
        elif sheet_name == "Occupations":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet(
                "Occupations"
            )
        elif sheet_name == "Groups":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Groups")
        elif sheet_name == "Places":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Places")
        elif sheet_name == "Events":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet(
                "Event Definitions"
            )
        elif sheet_name == "Group Entities":
            sheet_data = client.open("Group_Entities").sheet1
        elif sheet_name == "Josephis":
            sheet_data = client.open("Josephis_Überarbeitungsformular_ASB").worksheet(
                "Daten"
            )
        elif sheet_name == "Events Sheet":
            sheet_data = client.open("Events").sheet1
        elif sheet_name == "Sonstige Seelsorgen":
            sheet_data = client.open(
                "Mögliche Einträge - sonstige_Seelsorgetätigkeit"
            ).sheet1
        elif sheet_name == "Sonstige Amt":
            sheet_data = client.open("Mögliche Einträge - sonstiges_Amt").sheet1
        elif sheet_name == "Sonstige Taetigkeit":
            sheet_data = client.open("Mögliche Einträge - sonstige_Tätigkeit").sheet1
        else:
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Persons")
        self._data = sheet_data.get_all_records()

    def getData(self):
        return self._data

    def getValues(self):
        current = {}
        # Extract and print all of the values
        for val in self._data:

            current[str(val["Name"]).strip()] = val

        self._value = current
        return self._value

    def getSingleValues(self):
        for i in self._value:
            print(i)


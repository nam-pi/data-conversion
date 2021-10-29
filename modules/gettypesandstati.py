
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas
from typing import Dict, Optional, Type

class GetTypesAndStati:
    """An abstraction layer that provides data from tables in Google sheets."""
    _data: Dict
    _value: {}
    def __init__(self, 
        sheet_name: str):

        current = {}

        # use creds to create a client to interact with the Google Drive API
        # scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(".credentials.json")
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        if sheet_name == "Statuses":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Statuses")
        elif sheet_name == "Occupations":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Occupations")
        elif sheet_name == "Groups":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Groups")
        elif sheet_name == "Places":
            sheet_data = client.open("NAMPI Data Entry Form v2").worksheet("Places")

        self._data = sheet_data.get_all_records()
        # Extract and print all of the values
        for (val) in self._data:
            
            current[str(val["Name"]).strip()]= val

        self._value = current

    def getValues(self):
        return self._value
        
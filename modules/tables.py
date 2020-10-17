import os
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pandas import DataFrame
from typing import Optional, List, TypeVar


class Col_heading:
    author = "Author"
    comment = "Comment"
    community_astheim = "Community Astheim"
    community_gaming = "Community Gaming"
    earliest_date = "Earliest Possible Date"
    event_definition = "Event Definition"
    event_place = "Event Place"
    exact_date = "Exact Date"
    family_name = "Family name"
    geoname_id = "Geonames-ID"
    gnd_id = "GND ID"
    interpretation_date = "Interpretation Date"
    latest_date = "Latest Possible Date"
    name = "Name"
    person = "Person"
    religious_name = "Religious name"
    source = "Source"
    source_location = "Source Location"
    title = "Title"
    type = "Type"
    wikidata = "Wikidata"


class Tables:
    __cache_path: str
    __cache_validity_days: int
    births: DataFrame
    complex_events: DataFrame
    deaths: DataFrame
    groups: DataFrame
    object_creations: DataFrame
    objects: DataFrame
    occupations: DataFrame
    persons: DataFrame
    places: DataFrame
    sources: DataFrame
    statuses: DataFrame
    titles: DataFrame

    def __init__(
        self,
        cache_path: str,
        credentials_path: str,
        cache_validity_days: int,
    ):
        self.__cache_path = cache_path
        self.__cache_validity_days = cache_validity_days

        credentials = self.__load_credentials(credentials_path)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open("NAMPI Data Entry Form v2")

        self.births = self.__get_data(spreadsheet, "Births")
        self.complex_events = self.__get_data(spreadsheet, "Complex Events")
        self.deaths = self.__get_data(spreadsheet, "Deaths")
        self.groups = self.__get_data(spreadsheet, "Groups")
        self.object_creations = self.__get_data(spreadsheet, "Object Creations")
        self.objects = self.__get_data(spreadsheet, "Objects")
        self.occupations = self.__get_data(spreadsheet, "Occupations")
        self.persons = self.__get_data(spreadsheet, "Persons", numericise_ignore=[2, 5])
        self.places = self.__get_data(spreadsheet, "Places", numericise_ignore=[2, 6])
        self.sources = self.__get_data(spreadsheet, "Sources")
        self.statuses = self.__get_data(spreadsheet, "Statuses")
        self.titles = self.__get_data(spreadsheet, "Titles")

    def __use_cache(self, file: str) -> bool:
        if not os.path.exists(file):
            return False
        if self.__cache_validity_days == 0:
            return False
        elif self.__cache_validity_days == -1:
            return True
        else:
            file_time = os.path.getmtime(file)
            if (time.time() - file_time) / 3600 > 24 * self.__cache_validity_days:
                return False
            else:
                return True

    def __load_credentials(self, path):
        with open(path, "r") as credentials_file:
            data = credentials_file.read()
        credentials_json = json.loads(data)
        credentials_file.close()
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        return ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)

    def __get_data(
        self,
        spreadsheet: gspread.Spreadsheet,
        worksheet_name: str,
        numericise_ignore: Optional[List[int]] = None,
    ) -> DataFrame:
        cache_file_path = os.path.join(self.__cache_path, worksheet_name + ".csv")
        if self.__use_cache(cache_file_path):
            print("Read {} from cache".format(worksheet_name))
            return pd.read_csv(cache_file_path)
        else:
            print("Read {} from Google".format(worksheet_name))
            worksheet = spreadsheet.worksheet(worksheet_name)
            df: DataFrame = DataFrame(
                worksheet.get_all_records(
                    default_blank=None, numericise_ignore=numericise_ignore
                )
            ).dropna(how="all")
            df.to_csv(cache_file_path)
            return df

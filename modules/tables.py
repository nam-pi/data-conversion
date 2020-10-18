"""The module for the Table and related classes.

Classes:
    Column: Headings for columns in the Google sheet.
    Table: Names of the available tables.
    Tables: The tables of the Google sheet document as DataFrame objects.

"""
import json
import math
import os
import time
from numbers import Number
from typing import Any, Dict, List, Literal, Optional, TypeVar

import gspread
import pandas as pd
from modules.no_value import NoValue
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame


class Table(NoValue):
    """Names of the avaialable tables."""

    BIRTHS = "Births"
    COMPLEX_EVENTS = "Complex Events"
    DEATHS = "Deaths"
    GROUPS = "Groups"
    OBJECT_CREATIONS = "Object Creations"
    OBJECTS = "Objects"
    OCCUPATIONS = "Occupations"
    PERSONS = "Persons"
    PLACES = "Places"
    SOURCES = "Sources"
    STATUSES = "Statuses"
    TITLES = "Titles"


class Column:
    """Headings for the columns in the available tables."""

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
    """Bundles the Google Sheets tables as pandas dataframes."""

    __cache_path: str
    __cache_validity_days: int
    __tables: Dict[Table, DataFrame] = {}

    def __init__(
        self,
        cache_path: str,
        credentials_path: str,
        cache_validity_days: int,
    ):
        """Initialize the class.

        Parameters:
            cache_path (str): The path to cache the individual tables so they do not need to be refetched on each execution of the script. Needs to exist.
            credentials_path (str): The path to the Google Service Account credentials to access Google Sheets. Needs to exist.
            cache_validity_days (int): The number of days cached files stay valid and are not refetched.
        """
        self.__cache_path = cache_path
        self.__cache_validity_days = cache_validity_days

        credentials = self.__load_credentials(credentials_path)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open("NAMPI Data Entry Form v2")

        for _, member in Table.__members__.items():
            self.__tables[member] = self.__get_data(spreadsheet, member.value)

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

    def get_table(self, table: Table) -> DataFrame:
        """Get a table as a dataframe.

        Parameter:
            table (Table): The table to get.

        Returns:
            Table: The table.
        """
        return self.__tables[table]

    def get_from_table(
        self,
        table: Table,
        index_column: str,
        index_value: str,
        output_column: str,
    ) -> Optional[str]:
        """Get a specific value from the indicated table. The target row is specified by an index value in an index column and the actual returned value is taken from the output column.

        Parameters:
            table (Table): The table to search in.
            index_column (str): The column in which the index value has to be found.
            index_value (str): The value to be present in the index column to indicate the desired row in the table.
            output_column (str): The name of the column to get the desired value from the indicated row.

        Returns:
            Optional[str]: The desired value if it can be found.
        """
        if not index_value:
            return None
        df = self.__tables[table]
        indexed = df.set_index(index_column)
        row = indexed.loc[index_value]
        result = row[output_column]
        if isinstance(result, Number) and math.isnan(result):  # type: ignore
            return None
        elif isinstance(result, str) and not result:
            return None
        else:
            return result

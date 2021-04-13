"""The module for the Google Sheet datasource class.

Classes:
    Googlesheet
"""

import errno
import json
import logging
import os
import time
from typing import Dict, Optional, Type

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame

from modules.no_value import NoValue


class Google_sheet:
    """An abstraction layer that provides data from tables in Google sheets."""

    __cache_path: str
    __cache_validity_days: int
    __spreadsheet: gspread.Spreadsheet
    _tables: Dict[NoValue, DataFrame] = {}
    sheet_name: str

    def __init__(
        self,
        sheet_name: str,
        cache_path: str,
        credentials_path: str,
        cache_validity_days: int,
        Tables: Type[NoValue],
    ):
        """Initialize the class.

        Parameters:
            sheet_name: The name of the Google Sheet
            cache_path: The path to cache the individual tables so they do not need to be refetched on each execution of the script. Needs to exist.
            credentials_path: The path to the Google Service Account credentials to access Google Sheets. Needs to exist.
            cache_validity_days: The number of days cached files stay valid and are not refetched.
            Tables: The enum-like list of the table names.
        """
        self.__cache_path = cache_path
        self.__cache_validity_days = cache_validity_days
        self.sheet_name = sheet_name

        logging.info("Read Google Sheet data for '{}'".format(sheet_name))

        # Open spreadsheet
        credentials = self.__load_credentials(credentials_path)
        gc = gspread.authorize(credentials)
        self.__spreadsheet = gc.open(sheet_name)

        # Read all tables in the sheet
        for _, member in Tables.__members__.items():
            self._tables[member] = self._get_data(member.value)

        logging.info(
            "Finished reading Google Sheet data '{}'".format(sheet_name))

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

    def _get_data(self, table_name: str) -> DataFrame:
        cache_folder = os.path.join(self.__cache_path, self.sheet_name)
        try:
            os.makedirs(cache_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        cache_file_path = os.path.join(cache_folder, table_name + ".csv")
        if self.__use_cache(cache_file_path):
            logging.info("Read {} from cache".format(table_name))
            return pd.read_csv(cache_file_path, dtype=str, keep_default_na=False)
        else:
            logging.info("Read {} from Google".format(table_name))
            worksheet = self.__spreadsheet.worksheet(table_name)
            df: DataFrame = DataFrame(
                worksheet.get_all_records(
                    default_blank=None, numericise_ignore=["all"]
                ),
                dtype=str,
            ).dropna(how="all")
            df.to_csv(cache_file_path)
            return df

    def get_table(self, table: NoValue) -> DataFrame:
        """Get a table as a dataframe.

        Parameter:
            table: The table to get.

        Returns:
            The table.
        """
        return self._tables[table]

    def get_from_table(
        self,
        table: NoValue,
        index_column: str,
        index_value: Optional[str],
        output_column: str,
    ) -> Optional[str]:
        """Get a specific value from the indicated table. The target row is specified by an index value in an index column and the actual returned value is taken from the output column.

        Parameters:
            table: The table to search in.
            index_column: The column in which the index value has to be found.
            index_value: The value to be present in the index column to indicate the desired row in the table.
            output_column: The name of the column to get the desired value from the indicated row.

        Returns:
            The desired value if it can be found.
        """
        if not index_value:
            return None
        df = self._tables[table]
        indexed = df.set_index(index_column)
        try:
            row = indexed.loc[index_value]
            result = row[output_column]
            return str(result) if result else None
        except:
            logging.warning(
                "'{}' is not existing in table '{}' and column '{}'".format(
                    index_value, table.value, index_column
                )
            )

    def table_has_value(
        self, table: NoValue, column: str, value: Optional[str]
    ) -> bool:
        """Test if the table column has a specific value.

        Parameters:
            table: The table to check.
            column: The name of the column to look in.
            value: The value to find in the column.

        Returns:
            True if the value can be found, otherwise False.
        """
        if not value:
            return False
        df = self._tables[table]
        return value in df[column].values

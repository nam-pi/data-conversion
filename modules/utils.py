import getopt
import sys
import os
from rdflib import Namespace
import pandas as pd
import math
from numbers import Number
from typing import Optional

##
# Gets the command line options. Currently:
# -d : int
def get_opts():
    argv = sys.argv[1:]
    opts = dict(getopt.getopt(argv, "d:")[0])
    d = int(opts["-d"]) if "-d" in opts else 1
    return {"d": d}


##
# Creates a rdflib namespace using the NAMPI base url, a resource and a separator at the end
def ns(resource: str, hash_separator: bool = False) -> Namespace:
    return Namespace(
        "https://purl.org/nampi/{}{}".format(resource, "#" if hash_separator else "/")
    )


def get_df_value(
    df: pd.DataFrame, index_column: str, index_value: str, output_column: str
) -> Optional[str]:
    if not index_value:
        return None
    indexed = df.set_index(index_column)
    row = indexed.loc[index_value]
    result = row[output_column]
    if isinstance(result, Number) and math.isnan(result):
        return None
    elif isinstance(result, str) and not result:
        return None
    else:
        return result

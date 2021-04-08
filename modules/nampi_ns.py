"""The module for the Namespace class.

Classes:
    Namespace

"""
from rdflib import Namespace


def _ns(resource: str, hash_separator: bool = False) -> Namespace:
    return Namespace("https://purl.org/nampi/{}{}".format(resource, "#" if hash_separator else "/"))


class Nampi_ns:
    """A collection for namespaces to be used in the NAMPI input table conversion."""

    act = _ns("documentInterpretationAct")
    author = _ns("author")
    core = _ns("owl/core", hash_separator=True)
    event = _ns("event")
    group = _ns("group")
    mona = _ns("owl/monastic-life", hash_separator=True)
    object = _ns("object")
    occupation = _ns("occupation")
    person = _ns("person")
    place = _ns("place")
    source = _ns("source")
    status = _ns("status")

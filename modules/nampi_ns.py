"""The module for the Namespace class.

Classes:
    Namespace

"""
from rdflib import Namespace


def _ns(resource: str, hash_separator: bool = False) -> Namespace:
    return Namespace("https://purl.org/nampi/{}{}".format(resource, "#" if hash_separator else "/"))


class Nampi_ns:
    """A collection for namespaces to be used in the NAMPI input table conversion."""

    acts = _ns("documentInterpretationActs")
    core = _ns("owl/core", hash_separator=True)
    events = _ns("events")
    groups = _ns("groups")
    mona = _ns("owl/monastic-life", hash_separator=True)
    objects = _ns("objects")
    occupations = _ns("occupations")
    persons = _ns("persons")
    places = _ns("places")
    sources = _ns("sources")
    statuses = _ns("statuses")

"""The module for the Namespace class.

Classes:
    Namespace

"""
from rdflib import Namespace


def _ns(resource: str, hash_separator: bool = False) -> Namespace:
    return Namespace(
        "https://purl.org/nampi/{}{}".format(resource, "#" if hash_separator else "/")
    )


class Nampi_ns:
    """A collection for namespaces to be used in the NAMPI input table conversion."""

    core = _ns("owl/core", hash_separator=True)
    mona = _ns("owl/monastic-life", hash_separator=True)
    acts = _ns("documentInterpretationActs")
    events = _ns("events")
    persons = _ns("persons")
    groups = _ns("groups")
    places = _ns("places")
    sources = _ns("sources")
    objects = _ns("objects")

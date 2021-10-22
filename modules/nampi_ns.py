"""The module for the Namespace class.

Classes:
    Namespace

"""
from rdflib import Namespace

from modules.cli_param import Env


def _base_ns(resource: str) -> Namespace:
    return Namespace(
        Env.data_namespace_prefix + resource + "/"
        if Env.data_namespace_prefix.endswith("/")
        else Env.data_namespace_prefix + "/" + resource + "/"
    )


def _purl_ns(resource: str, hash_separator: bool = False) -> Namespace:
    return Namespace(
        "http://purl.org/nampi/{}{}".format(resource, "#" if hash_separator else "/")
    )


class Nampi_ns:
    """A collection for namespaces to be used in the NAMPI input table conversion."""

    act = _base_ns("acts")
    aspect = _base_ns("aspects")
    author = _base_ns("authors")
    core = _purl_ns("owl/core", hash_separator=True)
    event = _base_ns("events")
    group = _base_ns("groups")
    mona = _purl_ns("owl/monastic-life", hash_separator=True)
    object = _base_ns("objects")
    person = _base_ns("persons")
    place = _base_ns("places")
    source = _base_ns("sources")

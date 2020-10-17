from modules.utils import ns


class Namespace:
    core = ns("owl/core", hash_separator=True)
    mona = ns("owl/monastic-life", hash_separator=True)
    acts = ns("documentInterpretationActs")
    events = ns("events")
    persons = ns("persons")
    groups = ns("groups")
    places = ns("places")
    sources = ns("sources")
    objects = ns("objects")

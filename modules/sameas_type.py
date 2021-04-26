from rdflib import Namespace


class Sameas:
    __wikidata_ns = Namespace("https://www.wikidata.org/entity/")
    __geonames_ns = Namespace("https://sws.geonames.org/")
    __gnd_ns = Namespace("https://d-nb.info/gnd/")

    @classmethod
    def geonames(cls, id):
        return cls.__geonames_ns[id]

    @classmethod
    def wikidata(cls, id):
        return cls.__wikidata_ns[id]

    @classmethod
    def gnd(cls, id):
        return cls.__gnd_ns[id]

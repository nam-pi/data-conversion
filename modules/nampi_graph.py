from rdflib import URIRef, BNode, Literal, RDF, RDFS, XSD, Graph, Namespace
from typing import Optional, List, TypeVar, Dict, Union
from modules.rdf_namespaces import Namespace as Nampi_ns
from modules.tables import Tables
import uuid
from datetime import datetime


class Nampi_graph:
    __graph: Graph

    def __init__(self) -> None:
        self.__graph = Graph()
        self.__graph.bind("acts", Nampi_ns.acts)
        self.__graph.bind("core", Nampi_ns.core)
        self.__graph.bind("events", Nampi_ns.events)
        self.__graph.bind("groups", Nampi_ns.groups)
        self.__graph.bind("mona", Nampi_ns.mona)
        self.__graph.bind("objects", Nampi_ns.objects)
        self.__graph.bind("persons", Nampi_ns.persons)
        self.__graph.bind("places", Nampi_ns.places)
        self.__graph.bind("sources", Nampi_ns.sources)

    def __create_entity(self, ns: Namespace) -> URIRef:
        return ns[str(uuid.uuid4())]

    @staticmethod
    def date_time_literal(date_string: str) -> Literal:
        return Literal(datetime.strptime(date_string, "%Y-%m-%d"))

    @staticmethod
    def string_literal(string: str):
        return Literal(string, datatype=XSD.string)

    def add(self, subj: Union[URIRef, BNode], pred: URIRef, obj: Union[URIRef, BNode]):
        self.__graph.add((subj, pred, obj))

    def add_blind(self, type_uri: URIRef) -> BNode:
        node = BNode()
        self.add(node, RDF.type, type_uri)
        return node

    def add_resource(self, ns: Namespace, type_uri: URIRef) -> URIRef:
        node = self.__create_entity(ns)
        self.add(node, RDF.type, type_uri)
        return node

    def add_labeled_resource(
        self, ns: Namespace, type_uri: URIRef, label: str
    ) -> URIRef:
        query = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?subject WHERE {{ ?subject rdfs:label "{}"}}'.format(
            label
        )
        resources = self.__graph.query(query)
        if len(resources) == 0:
            node = self.add_resource(ns, type_uri)
            self.add(node, RDFS.label, Literal(label))
            return node
        else:
            for row in resources:
                return row[0]

    def serialize(self, format: str):
        return self.__graph.serialize(format=format).decode("utf-8")

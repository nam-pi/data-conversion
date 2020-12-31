"""The module for the Nampi_type class.

Classes:
    Nampi_type

"""
from modules.nampi_ns import Nampi_ns


class Nampi_type:
    """The various types namespaced to the NAMPI Core and Monastic Life ontologies."""

    class Core:
        """The types in the NAMPI Core ontology."""

        # Classes

        author = Nampi_ns.core.author
        automated_agent = Nampi_ns.core.automated_agent
        date = Nampi_ns.core.date
        document_interpretation_act = Nampi_ns.core.document_interpretation_act
        event = Nampi_ns.core.event
        identifier = Nampi_ns.core.identifier
        occupation = Nampi_ns.core.occupation
        person = Nampi_ns.core.person
        place = Nampi_ns.core.place
        source = Nampi_ns.core.source
        source_location = Nampi_ns.core.source_location
        status = Nampi_ns.core.status
        title = Nampi_ns.core.title

        # Object properties

        adds_status = Nampi_ns.core.adds_status
        assigns_name = Nampi_ns.core.assigns_name
        assigns_name_to = Nampi_ns.core.assigns_name_to
        assigns_title = Nampi_ns.core.assigns_title
        assigns_title_to = Nampi_ns.core.assigns_title_to
        changes_occupation_by = Nampi_ns.core.changes_occupation_by
        changes_occupation_of = Nampi_ns.core.changes_occupation_of
        changes_status_in = Nampi_ns.core.changes_status_in
        changes_status_of = Nampi_ns.core.changes_status_of
        ends_life_of = Nampi_ns.core.ends_life_of
        has_identifier = Nampi_ns.core.has_identifier
        has_interpretation = Nampi_ns.core.has_interpretation
        has_source = Nampi_ns.core.has_source
        has_source_location = Nampi_ns.core.has_source_location
        is_authored_by = Nampi_ns.core.is_authored_by
        is_authored_on = Nampi_ns.core.is_authored_on
        is_controlled_by = Nampi_ns.core.is_controlled_by
        removes_status = Nampi_ns.core.removes_status
        starts_life_of = Nampi_ns.core.starts_life_of
        starts_occupation = Nampi_ns.core.starts_occupation
        stops_occupation = Nampi_ns.core.stops_occupation
        takes_place_at = Nampi_ns.core.takes_place_at
        takes_place_not_earlier_than = Nampi_ns.core.takes_place_not_earlier_than
        takes_place_not_later_than = Nampi_ns.core.takes_place_not_later_than
        takes_place_on = Nampi_ns.core.takes_place_on

        # Data properties

        has_xsd_date_time = Nampi_ns.core.has_xsd_date_time
        has_xsd_string = Nampi_ns.core.has_xsd_string

    class Mona:
        """The types in the Monastic Life ontology."""

        # Classes

        benedictine_community = Nampi_ns.mona.benedictine_community
        birth = Nampi_ns.mona.birth
        canonesses_of_st_augustine = Nampi_ns.mona.canonesses_of_st_augustine
        canonesses_of_st_augustine_community = Nampi_ns.mona.canonesses_of_st_augustine_community
        carthusian_community = Nampi_ns.mona.carthusian_community
        christian_community = Nampi_ns.mona.christian_community
        christian_denomination = Nampi_ns.mona.christian_denomination
        christian_diocese = Nampi_ns.mona.christian_diocese
        christian_order = Nampi_ns.mona.christian_order
        christian_parish = Nampi_ns.mona.christian_parish
        death = Nampi_ns.mona.death
        dominican_community = Nampi_ns.mona.dominican_community
        family = Nampi_ns.mona.family
        family_member = Nampi_ns.mona.family_member
        family_name = Nampi_ns.mona.family_name
        given_name = Nampi_ns.mona.given_name
        religious_name = Nampi_ns.mona.religious_name
        roman_catholic_diocese = Nampi_ns.mona.roman_catholic_diocese
        roman_catholic_group = Nampi_ns.mona.roman_catholic_group
        roman_catholic_order = Nampi_ns.mona.roman_catholic_order
        roman_catholic_parish = Nampi_ns.mona.roman_catholic_parish

        # Object properties

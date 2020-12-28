"""The module for the Nampi_type class.

Classes:
    Nampi_type

"""
from modules.nampi_ns import Nampi_ns


class Nampi_type:
    """The various types namespaced to the NAMPI Core and Monastic Life ontologies."""

    class Core:
        """The types in the NAMPI Core ontology."""

        adds_group_status_as = Nampi_ns.core.adds_group_status_as
        adds_group_status_in = Nampi_ns.core.adds_group_status_in
        adds_group_status_to = Nampi_ns.core.adds_group_status_to
        assigns_appellation = Nampi_ns.core.assigns_appellation
        assigns_appellation_to = Nampi_ns.core.assigns_appellation_to
        date = Nampi_ns.core.date
        document_interpretation_act = Nampi_ns.core.document_interpretation_act
        ends_life_of = Nampi_ns.core.ends_life_of
        event = Nampi_ns.core.event
        family = Nampi_ns.mona.family
        family_member = Nampi_ns.mona.family_member
        family_name = Nampi_ns.core.family_name
        given_name = Nampi_ns.core.given_name
        has_date_time_representation = Nampi_ns.core.has_date_time_representation
        has_earliest_possible_date_time_representation = (
            Nampi_ns.core.has_earliest_possible_date_time_representation)
        has_interpretation = Nampi_ns.core.has_interpretation
        has_latest_possible_date_time_representation = (
            Nampi_ns.core.has_latest_possible_date_time_representation)
        has_source = Nampi_ns.core.has_source
        has_source_location = Nampi_ns.core.has_source_location
        has_string_representation = Nampi_ns.core.has_string_representation
        identifier = Nampi_ns.core.identifier
        is_authored_by = Nampi_ns.core.is_authored_by
        is_authored_on = Nampi_ns.core.is_authored_on
        person = Nampi_ns.core.person
        place = Nampi_ns.core.place
        removes_group_status_as = Nampi_ns.core.removes_group_status_as
        removes_group_status_in = Nampi_ns.core.removes_group_status_in
        removes_group_status_from = Nampi_ns.core.removes_group_status_from
        source = Nampi_ns.core.source
        source_location = Nampi_ns.core.source_location
        starts_life_of = Nampi_ns.core.starts_life_of
        status = Nampi_ns.core.status
        takes_place_after = Nampi_ns.core.takes_place_after
        takes_place_at = Nampi_ns.core.takes_place_at
        takes_place_before = Nampi_ns.core.takes_place_before
        takes_place_on = Nampi_ns.core.takes_place_on
        takes_place_sometime_between = Nampi_ns.core.takes_place_sometime_between
        unclear_date = Nampi_ns.core.unclear_date

    class Mona:
        """The types in the Monastic Life ontology."""

        benedictine_community = Nampi_ns.mona.benedictine_community
        canonesses_of_st_augustine = Nampi_ns.mona.canonesses_of_st_augustine
        canonesses_of_st_augustine_community = Nampi_ns.mona.canonesses_of_st_augustine_community
        carthusian_community = Nampi_ns.mona.carthusian_community
        christian_community = Nampi_ns.mona.christian_community
        christian_denomination = Nampi_ns.mona.christian_denomination
        christian_diocese = Nampi_ns.mona.christian_diocese
        christian_order = Nampi_ns.mona.christian_order
        christian_parish = Nampi_ns.mona.christian_parish
        dominican_community = Nampi_ns.mona.dominican_community
        religious_name = Nampi_ns.mona.religious_name
        religious_title = Nampi_ns.mona.religious_title
        roman_catholic_diocese = Nampi_ns.mona.roman_catholic_diocese
        roman_catholic_group = Nampi_ns.mona.roman_catholic_group
        roman_catholic_order = Nampi_ns.mona.roman_catholic_order
        roman_catholic_parish = Nampi_ns.mona.roman_catholic_parish

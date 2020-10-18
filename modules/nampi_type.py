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
        appellation_assignment = Nampi_ns.core.appellation_assignment
        assigns_appellation = Nampi_ns.core.assigns_appellation
        assigns_appellation_to = Nampi_ns.core.assigns_appellation_to
        birth = Nampi_ns.core.birth
        date = Nampi_ns.core.date
        death = Nampi_ns.core.death
        document_interpretation_act = Nampi_ns.core.document_interpretation_act
        ends_life_of = Nampi_ns.core.ends_life_of
        family_name = Nampi_ns.core.family_name
        has_date_time_representation = Nampi_ns.core.has_date_time_representation
        has_earliest_possible_date_time_representation = (
            Nampi_ns.core.has_earliest_possible_date_time_representation
        )
        has_interpretation = Nampi_ns.core.has_interpretation
        has_latest_possible_date_time_representation = (
            Nampi_ns.core.has_latest_possible_date_time_representation
        )
        has_source = Nampi_ns.core.has_source
        has_source_location = Nampi_ns.core.has_source_location
        has_string_representation = Nampi_ns.core.has_string_representation
        is_authored_by = Nampi_ns.core.is_authored_by
        is_authored_on = Nampi_ns.core.is_authored_on
        person = Nampi_ns.core.person
        place = Nampi_ns.core.place
        source = Nampi_ns.core.source
        source_location = Nampi_ns.core.source_location
        starts_life_of = Nampi_ns.core.starts_life_of
        takes_place_after = Nampi_ns.core.takes_place_after
        takes_place_at = Nampi_ns.core.takes_place_at
        takes_place_before = Nampi_ns.core.takes_place_before
        takes_place_on = Nampi_ns.core.takes_place_on
        takes_place_sometime_between = Nampi_ns.core.takes_place_sometime_between
        unclear_date = Nampi_ns.core.unclear_date

    class Mona:
        """The types in the Monastic Life ontology."""

        carthusian_order = Nampi_ns.mona.carthusian_order
        consecration = Nampi_ns.mona.consecration
        donatus = Nampi_ns.mona.donatus
        investiture = Nampi_ns.mona.investiture
        novice = Nampi_ns.mona.novice
        professed_member_of_a_religious_community = (
            Nampi_ns.mona.professed_member_of_a_religious_community
        )
        profession = Nampi_ns.mona.profession
        religious_name = Nampi_ns.mona.religious_name

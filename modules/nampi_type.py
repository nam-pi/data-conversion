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

        act = Nampi_ns.core.act
        aspect = Nampi_ns.core.aspect
        author = Nampi_ns.core.author
        automated_agent = Nampi_ns.core.automated_agent
        date = Nampi_ns.core.date
        event = Nampi_ns.core.event
        group = Nampi_ns.core.group
        identifier = Nampi_ns.core.identifier
        online_source = Nampi_ns.core.online_source
        person = Nampi_ns.core.person
        place = Nampi_ns.core.place
        source = Nampi_ns.core.source
        source_location = Nampi_ns.core.source_location
        title = Nampi_ns.core.title

        # Object properties

        adds_aspect = Nampi_ns.core.adds_aspect
        changes_aspect_related_to = Nampi_ns.core.changes_aspect_related_to
        ends_life_of = Nampi_ns.core.ends_life_of
        has_identifier = Nampi_ns.core.has_identifier
        has_interpretation = Nampi_ns.core.has_interpretation
        has_main_participant = Nampi_ns.core.has_main_participant
        has_other_participant = Nampi_ns.core.has_other_participant
        has_parent = Nampi_ns.core.has_parent
        has_source = Nampi_ns.core.has_source
        has_source_location = Nampi_ns.core.has_source_location
        is_authored_by = Nampi_ns.core.is_authored_by
        is_authored_on = Nampi_ns.core.is_authored_on
        is_controlled_by = Nampi_ns.core.is_controlled_by
        is_part_of = Nampi_ns.core.is_part_of
        removes_aspect = Nampi_ns.core.removes_aspect
        same_as = Nampi_ns.core.same_as
        starts_life_of = Nampi_ns.core.starts_life_of
        takes_place_at = Nampi_ns.core.takes_place_at
        takes_place_not_earlier_than = Nampi_ns.core.takes_place_not_earlier_than
        takes_place_not_later_than = Nampi_ns.core.takes_place_not_later_than
        takes_place_on = Nampi_ns.core.takes_place_on

        # Data properties

        has_value = Nampi_ns.core.has_value
        has_text = Nampi_ns.core.has_text
        has_date_time = Nampi_ns.core.has_date_time

        # has_xsd_date_time = Nampi_ns.core.has_xsd_date_time
        # has_xsd_string = Nampi_ns.core.has_xsd_string

    class Mona:
        """The types in the Monastic Life ontology."""

        # Other classes

        manuscript = Nampi_ns.mona.manuscript
        religious_title = Nampi_ns.mona.religious_title

        # Names

        family_name = Nampi_ns.mona.family_name
        given_name = Nampi_ns.mona.given_name
        religious_name = Nampi_ns.mona.religious_name

        # Groups

        christian_denomination = Nampi_ns.mona.christian_denomination
        diocese = Nampi_ns.mona.diocese
        family = Nampi_ns.mona.family
        historical_diocese = Nampi_ns.mona.historical_diocese
        monastic_community = Nampi_ns.mona.monastic_community
        parish = Nampi_ns.mona.parish
        polity = Nampi_ns.mona.polity
        religious_denomination = Nampi_ns.mona.religious_denomination
        religious_order = Nampi_ns.mona.religious_order
        religious_polity = Nampi_ns.mona.religious_polity
        historic_diocese = Nampi_ns.mona.historic_diocese

        # Aspect types

        academic_degree = Nampi_ns.mona.academic_degree
        clergy = Nampi_ns.mona.clergy
        community_subsacristan = Nampi_ns.mona.community_subsacristan
        community_superior = Nampi_ns.mona.community_superior
        member_of_a_religious_community = Nampi_ns.mona.member_of_a_religious_community
        member_of_a_religious_community_with_manual_focus = (
            Nampi_ns.mona.member_of_a_religious_community_with_manual_focus
        )
        member_of_a_religious_community_with_spiritual_focus = (
            Nampi_ns.mona.member_of_a_religious_community_with_spiritual_focus
        )
        procurator = Nampi_ns.mona.procurator
        professed_member_of_a_religious_community = (
            Nampi_ns.mona.professed_member_of_a_religious_community
        )
        vice_community_superior = Nampi_ns.mona.vice_community_superior
        visitator = Nampi_ns.mona.visitator
        monastic_office_with_spiritual_focus = (
            Nampi_ns.mona.monastic_office_with_spiritual_focus
        )
        monastic_office_with_manual_focus = (
            Nampi_ns.mona.monastic_office_with_manual_focus
        )
        monastic_office = Nampi_ns.mona.monastic_office
        member_of_a_religious_community_visiting = (
            Nampi_ns.mona.member_of_a_religious_community_visiting
        )
        religious_life_outside_a_community = (
            Nampi_ns.mona.religious_life_outside_a_community
        )
        office_in_a_diocese = Nampi_ns.mona.office_in_a_diocese

        administration_of_a_community = Nampi_ns.mona.administration_of_a_community
        associated_parish_clergy = Nampi_ns.mona.associated_parish_clergy
        official = Nampi_ns.mona.official
        profession = Nampi_ns.mona.profession
        rule_of_a_community = Nampi_ns.mona.rule_of_a_community

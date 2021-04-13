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
        group = Nampi_ns.core.group
        identifier = Nampi_ns.core.identifier
        occupation = Nampi_ns.core.occupation
        online_source = Nampi_ns.core.online_source
        online_resource = Nampi_ns.core.online_resource
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
        has_online_source = Nampi_ns.core.has_online_source
        has_source = Nampi_ns.core.has_source
        has_source_location = Nampi_ns.core.has_source_location
        is_authored_by = Nampi_ns.core.is_authored_by
        is_authored_on = Nampi_ns.core.is_authored_on
        is_controlled_by = Nampi_ns.core.is_controlled_by
        is_part_of = Nampi_ns.core.is_part_of
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
        has_url = Nampi_ns.core.has_url

    class Mona:
        """The types in the Monastic Life ontology."""

        # Other classes

        manuscript = Nampi_ns.mona.manuscript
        page = Nampi_ns.mona.page
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

        # Status types

        academic_degree = Nampi_ns.mona.academic_degree
        clergy = Nampi_ns.mona.clergy
        community_hospes = Nampi_ns.mona.community_hospes
        community_subsacristan = Nampi_ns.mona.community_subsacristan
        community_superior = Nampi_ns.mona.community_superior
        community_member = Nampi_ns.mona.community_member
        member_with_manual_focus = Nampi_ns.mona.member_with_manual_focus
        member_with_spiritual_focus = Nampi_ns.mona.member_with_spiritual_focus
        monastic_office = Nampi_ns.mona.monastic_office
        procurator = Nampi_ns.mona.procurator
        professed_member = Nampi_ns.mona.professed_member
        vice_community_superior = Nampi_ns.mona.vice_community_superior
        visitator = Nampi_ns.mona.visitator

        # Occupation types

        administration_of_a_community = Nampi_ns.mona.administration_of_a_community
        associated_parish_clergy = Nampi_ns.mona.associated_parish_clergy
        clergy = Nampi_ns.mona.clergy_occupation
        official = Nampi_ns.mona.official
        profession = Nampi_ns.mona.profession
        rule_of_a_community = Nampi_ns.mona.rule_of_a_community

        # Object properties

        has_paged_source = Nampi_ns.mona.has_paged_source

        # Data properties

        has_page_number = Nampi_ns.mona.has_page_number

from modules.rdf_namespaces import Namespace


class Type:
    class Core:
        adds_group_status_as = Namespace.core.adds_group_status_as
        adds_group_status_in = Namespace.core.adds_group_status_in
        adds_group_status_to = Namespace.core.adds_group_status_to
        appellation_assignment = Namespace.core.appellation_assignment
        assigns_appellation = Namespace.core.assigns_appellation
        assigns_appellation_to = Namespace.core.assigns_appellation_to
        birth = Namespace.core.birth
        date = Namespace.core.date
        death = Namespace.core.death
        document_interpretation_act = Namespace.core.document_interpretation_act
        ends_life_of = Namespace.core.ends_life_of
        family_name = Namespace.core.family_name
        has_date_time_representation = Namespace.core.has_date_time_representation
        has_earliest_possible_date_time_representation = (
            Namespace.core.has_earliest_possible_date_time_representation
        )
        has_interpretation = Namespace.core.has_interpretation
        has_latest_possible_date_time_representation = (
            Namespace.core.has_latest_possible_date_time_representation
        )
        has_source = Namespace.core.has_source
        has_source_location = Namespace.core.has_source_location
        has_string_representation = Namespace.core.has_string_representation
        is_authored_by = Namespace.core.is_authored_by
        is_authored_on = Namespace.core.is_authored_on
        person = Namespace.core.person
        place = Namespace.core.place
        source = Namespace.core.source
        source_location = Namespace.core.source_location
        starts_life_of = Namespace.core.starts_life_of
        takes_place_after = Namespace.core.takes_place_after
        takes_place_at = Namespace.core.takes_place_at
        takes_place_before = Namespace.core.takes_place_before
        takes_place_on = Namespace.core.takes_place_on
        takes_place_sometime_between = Namespace.core.takes_place_sometime_between
        unclear_date = Namespace.core.unclear_date

    class Mona:
        carthusian_order = Namespace.mona.carthusian_order
        consecration = Namespace.mona.consecration
        donatus = Namespace.mona.donatus
        investiture = Namespace.mona.investiture
        novice = Namespace.mona.novice
        professed_member_of_a_religious_community = (
            Namespace.mona.professed_member_of_a_religious_community
        )
        profession = Namespace.mona.profession
        religious_name = Namespace.mona.religious_name

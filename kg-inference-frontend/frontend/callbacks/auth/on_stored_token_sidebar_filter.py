from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate

from data.dict_key import DictKey
from layout.utils import make_toast, ToastType
from query.api import get_rules, AuthenticationError, APIError
from data.rule import Rule

GENERALIZE_SIMILARITY_ID = "sim_rule"

SUB_SIMILARITY_RULE_IDS = {
    "https://bbp.epfl.ch/neurosciencegraph/data/9d64dc0d-07d1-4624-b409-cdc47ccda212":
        DictKey.BRAIN_REGIONS
}


def on_stored_token_sidebar_filter(app):
    @app.callback(
        Output(component_id="stored_rules", component_property="data"),
        Output(component_id="toast_container_rules", component_property="children"),
        Output(component_id="rule_fetching_loader", component_property="children"),
        Output(component_id="selected_rule", component_property="clear_data"),
        Input(component_id="stored_token", component_property="data"),
        Input(component_id="stored_filters", component_property="data"),
        # State(component_id="contributor_dropdown", component_property="value"),
    )
    def on_stored_token_sidebar_filter_callback(token, search_filters):
        # contributors

        if token:
            if token is None:
                return None, make_toast(ToastType.ERROR, "Missing Authentication Token"), \
                    no_update, True
            try:
                rules_class = get_rules(token, search_filters)

                rules = [rule for rule in rules_class if rule.id not in SUB_SIMILARITY_RULE_IDS]
                sim_rules = dict(
                    (SUB_SIMILARITY_RULE_IDS[rule.id], rule)
                    for rule in rules_class if rule.id in SUB_SIMILARITY_RULE_IDS
                )

                if len(sim_rules) != 0:
                    rules.append(Rule(
                        sub_rules=sim_rules,
                        name="Generalise by similarity in a BBP ontology (e.g. cell type, "
                             "brain region)",
                        description="""
                        Given an entity type (e.g NeuronMorphology, Trace, cell type, ...) 
                        linked with a value in an ontology (e.g. Brain Region, M Type, E Type, 
                        Species), generalise to entities associated with similar values in the 
                        ontology
                        """,
                        id=GENERALIZE_SIMILARITY_ID,
                        resource_type="Entity",
                        input_parameters=[],
                        nexus_link=None
                    ))

                rules = [Rule.class_to_store(rule) for rule in rules]

                return rules, make_toast(ToastType.INFORMATION, f"Fetched {len(rules)} rules"), \
                    no_update, True

            except (AuthenticationError, APIError) as e:
                return None, make_toast(ToastType.ERROR, str(e)), no_update, True

        raise PreventUpdate

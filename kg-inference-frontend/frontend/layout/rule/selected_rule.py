from typing import Dict, List

from dash import html, dcc

from callbacks.auth.on_stored_token_sidebar_filter import GENERALIZE_SIMILARITY_ID
from data.rule import Rule
from layout.rule.inference_inputs import generic_input_groups, get_limit_form_control
from layout.rule.custom_rules.generalize_hierarchy_rule import (
    generalise_hierarchy_input_groups,
    GENERALIZE_HIERARCHY_ID
)
from layout.rule.custom_rules.generalize_similarity_rule import (
    generalise_similarity_input_groups,
    DEFAULT_SIMILARITY
)
from query.forge import NM_RULE_IDS
from layout.rule.custom_rules.nm_rules import nm_rules_input_groups


def build_inputs(rule, token, sidebar_content=None, stored_filters=None):
    # input_groups = [get_limit_form_control(rule.id)]
    input_groups = []

    if len(rule.input_parameters) > 0 or rule.id == GENERALIZE_SIMILARITY_ID:
        if rule.id == GENERALIZE_SIMILARITY_ID:
            fc = generalise_similarity_input_groups
        else:
            if rule.id == GENERALIZE_HIERARCHY_ID:
                fc = generalise_hierarchy_input_groups
            elif rule.id in NM_RULE_IDS:
                fc = nm_rules_input_groups
            else:
                fc = generic_input_groups

        prepend = fc(rule, token, sidebar_content=sidebar_content, stored_filters=stored_filters)
        input_groups = prepend + input_groups

    return html.Div(children=[
        html.H5(children="Inputs: "),
        html.Div(children=input_groups, className="form-row")
    ])


def build_selected_rule(
        rule: Dict, token: str, sidebar_content: Dict[str, Dict] = None,
        stored_filters: Dict[str, List] = None
):
    rule = Rule.store_to_class(rule)

    inputs = build_inputs(rule, token=token, stored_filters=stored_filters,
                          sidebar_content=sidebar_content)

    def get_nexus_link():
        if rule.nexus_link is not None:
            return rule.nexus_link
        if rule.sub_rules is not None and len(rule.sub_rules) != 0:
            return rule.sub_rules[DEFAULT_SIMILARITY].nexus_link
        return None

    link = dcc.Link(
        children="For feedback, use the Jira tool integrated in the rule page of Nexus Fusion",
        href=get_nexus_link(),
        target="_blank"
    ) if get_nexus_link() is not None else html.Div()

    return [
        html.H5(children="Description: "),
        html.P(children=rule.description),
        link,
        html.Hr(),
        inputs,
        html.Div(children=[
            html.Button(children="Infer", id="infer_button", className="btn btn-dark mt-2"),
            html.Div(id="infer_message")
        ], className="form-row")
    ], html.H5(rule.name)

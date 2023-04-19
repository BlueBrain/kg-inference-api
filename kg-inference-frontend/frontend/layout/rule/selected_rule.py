from dash import html, dcc

from data.rule import Rule
from layout.rule.inference_inputs import generic_input_groups, get_limit_form_control
from layout.rule.custom_rules.generalize_hierarchy_rule import generalise_context_input_groups, \
    GENERALIZE_HIERARCHY_ID
from query.forge import NM_RULE_IDS
from layout.rule.custom_rules.nm_rules import nm_rules_input_groups


def build_inputs(rule, token, sidebar_content=None, stored_filters=None):
    # input_groups = [get_limit_form_control(rule.id)]
    input_groups = []
    if len(rule.input_parameters) > 0:

        fc = generalise_context_input_groups if rule.id == GENERALIZE_HIERARCHY_ID \
            else (nm_rules_input_groups if rule.id in NM_RULE_IDS else generic_input_groups)

        prepend = fc(rule, token, sidebar_content=sidebar_content, stored_filters=stored_filters)
        input_groups = prepend + input_groups

    return html.Div(children=[
        html.H5(children="Inputs: "),
        html.Div(children=input_groups, className="form-row")
    ])


def build_selected_rule(rule, token, sidebar_content=None, stored_filters=None):

    rule = Rule.store_to_class(rule)

    inputs = build_inputs(rule, token=token, stored_filters=stored_filters,
                          sidebar_content=sidebar_content)

    return [
        html.H5(children="Description: "),
        html.P(children=rule.description),
        dcc.Link(children=
                 "For feedback, use the Jira tool integrated in the rule page of Nexus Fusion",
                 href=rule.nexus_link, target="_blank"),
        html.Hr(),
        inputs,
        html.Div(children=[
            html.Button(children="Infer", id="infer_button", className="btn btn-dark mt-2"),
            html.Div(id="infer_message")
        ], className="form-row")
    ], html.H5(rule.name)

from dash import Input, Output, State, html

from query.forge import NM_RULE_IDS
from layout.layout import result_view, to_be_filled
from layout.rule.selected_rule import build_selected_rule


def on_selected_rule_update(app):
    @app.callback(
        Output(component_id="selected_rule_title", component_property="children"),
        Output(component_id="selected_rule_view", component_property="children"),
        Output(component_id="input_parameters", component_property="clear_data"),
        Output(component_id="nm_container", component_property="children"),
        Output(component_id="collapse_nm", component_property="className", allow_duplicate=True),
        Input(component_id="selected_rule", component_property="data"),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data"),
        prevent_initial_call=True
    )
    def on_selected_rule_update_callback(rule, sidebar_content, token, stored_filters):

        if rule is None:
            return (
                html.H5("Selected Rule"),
                to_be_filled("selected_view_id"),
                True,
                result_view(results=False, empty=True),
                "card-body collapse"
            )
            # Resetting nm_container = div with id collapse_nm because
            # callback is failing if the element doesn't exist on_infer_press/on_collapse_nm_click

        view, title = build_selected_rule(
            rule=rule, token=token, sidebar_content=sidebar_content,
            stored_filters=stored_filters
        )

        empty = not rule["id"] in NM_RULE_IDS
        # empty means the minimal content for things
        # to work will be put (stores due to callbacks including them). If not empty,
        # the container is filled with the neuron morphology list table, and selected neuron
        # morphology view

        return (
            title,
            view,
            True,
            result_view(results=False, empty=empty),
            "card-body collapse show"
        )

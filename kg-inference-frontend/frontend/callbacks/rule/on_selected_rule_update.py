from dash import Input, Output, State, html

from query.forge import NM_RULE_IDS
from layout.layout import result_view, to_be_filled
from layout.rule.selected_rule import build_selected_rule


def on_selected_rule_update(app):
    @app.callback(
        Output(component_id='selected_rule_title', component_property="children"),
        Output(component_id="selected_rule_view", component_property="children"),
        Output(component_id="input_parameters", component_property="clear_data"),
        Output(component_id='nm_container', component_property='children'),
        Input(component_id='selected_rule', component_property='data'),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data")
    )
    def on_selected_rule_update_callback(rule, sidebar_content, token, stored_filters):

        if rule is not None:

            view, title = build_selected_rule(
                rule=rule, token=token, sidebar_content=sidebar_content,
                stored_filters=stored_filters
            )

            nm = result_view(False) if rule["id"] in NM_RULE_IDS else \
                result_view(results=False, empty=True)

            return title, view, True, nm

        return html.H5("Selected Rule"), to_be_filled("selected_view_id"), True, \
            result_view(results=False, empty=True)

    # Resetting nm_container = div with id collapse_nm because
    # callback is failing if the element doesn't exist on_infer_press/on_collapse_nm_click

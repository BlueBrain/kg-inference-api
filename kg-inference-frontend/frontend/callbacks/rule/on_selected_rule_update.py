from dash import Input, Output, State, no_update
from layout.utils import grey_box
from layout.rule.selected_rule import build_selected_rule


def on_selected_rule_update(app):
    @app.callback(
        Output(component_id='selected_rule_view', component_property="children"),
        Output(component_id='selected_rule_title', component_property="children"),
        Output(component_id="selected_rule_loader", component_property="children"),
        Output(component_id='stored_results', component_property='clear_data'),
        Output(component_id='selected_result', component_property='clear_data'),
        Input(component_id='selected_rule', component_property='data'),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data"),
        State(component_id='stored_results', component_property='modified_timestamp'),
        State(component_id='selected_result', component_property='modified_timestamp'),
    )
    def on_selected_rule_update_callback(rule, sidebar_content, token, stored_filters, stored_results_timestamp,
                                         selected_result_timestamp):

        clear_if_not_empty = stored_results_timestamp != -1  # only clear if the store has already been changed
        clear_if_not_empty2 = selected_result_timestamp != -1

        if rule is not None:

            view, title = build_selected_rule(rule, token=token,
                                              sidebar_content=sidebar_content, stored_filters=stored_filters)
            return view, title, no_update, clear_if_not_empty, clear_if_not_empty2

        return grey_box(), "Selected Rule", no_update, clear_if_not_empty, clear_if_not_empty2

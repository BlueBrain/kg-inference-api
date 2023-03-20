from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from layout.utils import make_toast, ToastType
from data.rule import Rule


def on_rule_row_select(app):

    @app.callback(
        Output(component_id='selected_rule', component_property='data'),
        Output(component_id='toast_container_rules_sidebar', component_property="children"),
        Input(component_id='datatable_rules', component_property='selected_row_ids'),
        State(component_id="stored_rules", component_property="data"),
        State(component_id="sidebar_content", component_property="data")
    )
    def on_rule_row_select_callback(selected_row_ids, stored_rules, sidebar_content):
        if selected_row_ids and selected_row_ids[0]:
            if sidebar_content is None:
                return None, make_toast(ToastType.WARNING, "Waiting for the sidebar to load")
            stored_rules_class = [Rule.store_to_class(rule) for rule in stored_rules]
            idx = selected_row_ids[0]
            rule = next(r for r in stored_rules_class if r.id == idx)
            return Rule.class_to_store(rule), no_update

        raise PreventUpdate

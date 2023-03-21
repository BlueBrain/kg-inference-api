from dash import Input, Output
from dash.exceptions import PreventUpdate
from layout.rule.rule_table import build_rule_table


def on_stored_rules_update(app):
    @app.callback(
        Output(component_id='rule_list', component_property='children'),
        Input(component_id='stored_rules', component_property='data')
    )
    def on_stored_rules_update_callback(stored_rules):
        if stored_rules is not None:
            return build_rule_table(stored_rules)
        raise PreventUpdate

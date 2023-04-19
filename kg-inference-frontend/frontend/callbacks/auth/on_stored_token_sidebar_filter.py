from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from layout.utils import make_toast, ToastType
from query.api import get_rules, AuthenticationError, APIError
from data.rule import Rule


def on_stored_token_sidebar_filter(app):
    @app.callback(
        Output(component_id='stored_rules', component_property='data'),
        Output(component_id='toast_container_rules', component_property="children"),
        Output(component_id="rule_fetching_loader", component_property="children"),
        Output(component_id='selected_rule', component_property='clear_data'),
        Input(component_id='stored_token', component_property='data'),
        Input(component_id='stored_filters', component_property='data'),
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
                rules = [Rule.class_to_store(rule) for rule in rules_class]

                return rules, make_toast(ToastType.INFORMATION, f"Fetched {len(rules)} rules"), \
                    no_update, True

            except (AuthenticationError, APIError) as e:
                return None, make_toast(ToastType.ERROR, str(e)), no_update, True

        raise PreventUpdate

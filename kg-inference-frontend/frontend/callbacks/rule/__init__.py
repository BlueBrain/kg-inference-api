from callbacks.rule.on_rule_row_select import on_rule_row_select
from callbacks.rule.on_selected_rule_update import on_selected_rule_update
from callbacks.rule.on_stored_rules_update import on_stored_rules_update
from callbacks.rule.on_generalized_field_name_change import on_generalized_field_name_change
from callbacks.rule.on_infer_press import on_infer_press


def get_rule_callbacks(app):
    on_infer_press(app)
    on_generalized_field_name_change(app)
    on_stored_rules_update(app)
    on_selected_rule_update(app)
    on_rule_row_select(app)

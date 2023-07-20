from callbacks.result.on_plot_control_change import on_plot_control_change
from callbacks.result.on_result_select import on_result_select
from callbacks.result.on_chart_control_change import on_chart_control_change
from callbacks.result.on_stored_results_update import on_stored_results_update
from callbacks.result.on_stored_selected_result_update import on_stored_selected_result_update


def get_result_callbacks(app):
    on_result_select(app)
    on_chart_control_change(app)
    on_stored_results_update(app)
    on_stored_selected_result_update(app)
    on_plot_control_change(app)

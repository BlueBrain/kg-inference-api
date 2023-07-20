from dash import Input, Output, State, callback_context
from dash.exceptions import PreventUpdate

from data.result.attribute import Attribute
from data.result.result_resource import ResultResource
from layout.result.result_plot import build_result_plot, prepare_data


def on_plot_control_change(app):
    @app.callback(
        Output(component_id="plot_container", component_property="children"),
        Output(component_id="prepared_plot_data", component_property="data", allow_duplicate=True),
        Input(component_id="plot_legend_picker", component_property="value"),
        Input(component_id="iteration_slider", component_property="value"),
        Input(component_id="perplexity_slider", component_property="value"),
        State(component_id="prepared_plot_data", component_property="data"),
        State(component_id="stored_results", component_property="data"),
        State(component_id="selected_rule", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="selected_nm", component_property="data"),
        prevent_initial_call=True
    )
    def on_plot_control_change_callback(
            legend_picker_value, iteration_value, perplexity_value,
            plot_data, results, rule, token, selected_nm
    ):

        if callback_context.triggered_id == "plot_legend_picker" and plot_data is not None:
            return (
                build_result_plot(
                    legend_field_name=Attribute(legend_picker_value),
                    prepared_data=plot_data
                ),
                plot_data
            )

        if callback_context.triggered_id in ["iteration_slider", "perplexity_slider"]:
            load = True

            result_dict = dict(
                (key, ResultResource.store_to_class(val))
                for key, val in results.items()
            )
            prepared_data = prepare_data(
                results=result_dict,
                rule=rule,
                token=token,
                selected_nm=ResultResource.store_to_class(selected_nm),
                load=load,
                perplexity=perplexity_value,
                nb_iterations=iteration_value
            )

            return (
                build_result_plot(
                    legend_field_name=Attribute(legend_picker_value),
                    prepared_data=prepared_data
                ),
                prepared_data
            )

        raise PreventUpdate

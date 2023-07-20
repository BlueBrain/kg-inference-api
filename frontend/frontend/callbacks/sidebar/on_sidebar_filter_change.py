from dash import Input, Output, html


def on_sidebar_filter_change(app):
    @app.callback(
        Output(component_id="search_filter_summary", component_property="children"),
        Input(component_id="datatype_dropdown", component_property="value"),
        Input(component_id="brain_region_dropdown", component_property="value"),
        Input(component_id="cell_type_dropdown", component_property="value"),
        # Input(component_id="contributor_dropdown", component_property="value"),
    )
    def on_sidebar_filter_change_callback(datatypes, brain_regions, cell_types):  # , contributors):
        def strify(i):
            return ", ".join(i) if i else "Any"

        return html.P(children=[
            "You have selected:", html.Br(),
            f"- Datatypes: {strify(datatypes)}", html.Br(),
            # f"- Contributors: {strify(contributors)}", html.Br(),
            f"- Brain Regions: {strify(brain_regions)}", html.Br(),
            f"- Cell Types: {strify(cell_types)}", html.Br()
        ])


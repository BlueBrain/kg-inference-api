from dash import html, dcc


def build_sidebar(brain_regions, data_types, cell_types, contributors):
    def to_dropdown_format(el_list): return [
        {"value": el.id, "label": el.name}
        for el in el_list
    ]

    def make_dropdown(label, dropdown_id, values): return html.Div(children=[
        html.H6(children=label),
        dcc.Dropdown(
            options=to_dropdown_format(values),
            id=dropdown_id,
            multi=True
        ),
    ], className="form-group mt-2")

    return [
        make_dropdown(label="By targeted data type", dropdown_id='datatype_dropdown', values=data_types),
        make_dropdown(label="By brain region", dropdown_id='brain_region_dropdown', values=brain_regions),
        make_dropdown(label="By cell type", dropdown_id='cell_type_dropdown', values=cell_types),
        # make_dropdown(label="By contributor", dropdown_id='contributor_dropdown', values=contributors),
        html.Div(className="mt-4", id='search_filter_summary'),
        html.Button(children="Filter Rules", id="filter_rules_button", className="btn btn-dark"),
    ]


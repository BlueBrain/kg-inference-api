from dash import html, dcc
from layout.auth.auth import auth
from layout.utils import grey_box


def to_be_filled(id_str):
    return html.Div(id=id_str, className="px-2 py-4",
                    children=grey_box(), style={"height": "100%"})


confluence_link = \
    "https://bbpteam.epfl.ch/project/spaces/display/BBKG/Inference+and+Data+Generalization+Rules"


def result_view(results: bool, empty: bool = False):
    """
    Result view used in order to display neuron morphology list/selected neuron morphology
    And inference results/selected results
    @param results: True if results view, False if neuron morphology view
    @type: bool
    @param empty: Render it empty or with its body. Necessary because some callbacks require
    some html element ids to exist, so the div is rendered with no visible content for these
    callbacks not to complain
    @type: bool
    """

    list_title = "Inference Results" if results else "Neuron Morphology List"
    fetching_loader_id = "result_fetching_loader" if results else "nm_fetching_loader"
    list_div = "result_list" if results else "nm_list"
    result_store_id = "stored_results" if results else "stored_nm"

    selected_title = "Selected Result" if results else "Selected Neuron Morphology"
    selected_title_id = "selected_result_title" if results else "selected_nm_title"
    selected_loader_id = "selected_result_loader" if results else "selected_nm_loader"
    selected_div = "selected_result_view" if results else "selected_nm_view"
    selected_store_id = "selected_result" if results else "selected_nm"
    collapse_id = "collapse_result" if results else "collapse_nm"

    body = [
        html.Div(children=[
            html.Div(className="col-xl-8 col-12", children=[
                html.Div(children=html.H5(list_title),
                         className="d-flex justify-content-center border-bottom"),
                dcc.Loading(id=fetching_loader_id, type="circle",
                            children=[to_be_filled(list_div)]),

                dcc.Store(id=result_store_id)
            ]),

            html.Div(className="col-xl-4 col-12", children=[
                html.Div(children=html.H5(selected_title), id=selected_title_id,
                         className="d-flex justify-content-center border-bottom"),
                dcc.Loading(id=selected_loader_id, type="circle",
                            children=[to_be_filled(selected_div)]),

                dcc.Store(id=selected_store_id)
            ]),
        ], className="row"),
    ] if not empty else [dcc.Store(id=selected_store_id)]

    return html.Div(className="card mt-4", children=[
        html.Button(className="dropdown-toggle", style={"border": "none"},
                    id=f"button_{collapse_id}",
                       ** {"data-bs-toggle": "collapse", "data-bs-target": f"#{collapse_id}"}),
        html.Div(className="card-body", id=collapse_id, children=html.Div(children=body))
    ])


page = html.Div(children=[

    html.Div(style={"zIndex": 900, "position": "relative"}, children=[
        html.Div(style={"position": "fixed", "top": 66, "right": 10, "width": 350}, children=[
            html.Div(id="toast_container_rules"),
            html.Div(id="toast_container_rules_sidebar"),
            html.Div(id="toast_container_token"),
            html.Div(id="toast_container_sidebar_fetch"),
            html.Div(id="toast_container_nm_fetch"),
            html.Div(id="toast_container_infer_press"),
            html.Div(id="toast_container_results_infer"),
            html.Div(id="toast_container_results_table"),
        ])
    ]),

    html.Div(id="header", children=[
        html.Div(className="col-xl-8 col-12", children=[
            html.H4("Knowledge Graph Inference Rules"),
            html.Span("In order to request a new rule, follow the instruction on the "),
            dcc.Link("confluence page", href=confluence_link, target="_blank"),
        ]),
        html.Div(className="d-flex justify-content-end col-xl-4 col-12", children=auth),
        dcc.Store(id="stored_token", storage_type="session"),
    ], className="row mt-4"),

    html.Div(className="card mt-4", children=[
        html.Button(className="dropdown-toggle", style={"border": "none"},
                    **{"data-bs-toggle": "collapse", "data-bs-target": "#collapse_rule"}),
        html.Div(className="card-body", id="collapse_rule", children=html.Div([
            html.Div(className="col-xl-3 col-md-4 col-12", children=[

                html.Div(children=html.H5("Search Data Generalization Rules"),
                         className="d-flex justify-content-center border-bottom"),

                dcc.Loading(id="sidebar_fetching_loader", type="circle",
                            children=[to_be_filled("sidebar")]),

                dcc.Store(id="sidebar_content"),
                dcc.Store(id="stored_filters")
            ]),

            html.Div(className="col-xl-5 col-md-8 col-12", children=[

                html.Div(children=html.H5("Rule Search Results"),
                         className="d-flex justify-content-center border-bottom"),

                dcc.Loading(id="rule_fetching_loader", type="circle",
                            children=[to_be_filled("rule_list")]),
                dcc.Store(id="stored_rules")

            ]),

            html.Div(className="col-xl-4 col-12", children=[
                html.Div(children=html.H5("Selected Rule"), id="selected_rule_title",
                         className="d-flex justify-content-center border-bottom"),
                html.Div(to_be_filled("selected_rule_view")),
                dcc.Store(id="selected_rule"),
                dcc.Store(id="input_parameters")

            ]),

        ], className="row"))
    ]),
    html.Div(id="nm_container", children=result_view(results=False, empty=True)),
    dcc.Store(id="prepared_plot_data"),  # TODO Place elsewhere most likely
    # callback is failing if the element doesn't exist on_infer_press/on_collapse_nm_click
    result_view(True),

], className="container-fluid")

from dash import html, dcc
from layout.auth.auth import auth
from layout.utils import grey_box


def to_be_filled(id_str):
    return html.Div(id=id_str, className="border-top px-2 py-4",
                    children=grey_box(), style={"height": "100%"})


page = html.Div(children=[

    html.Div(style={"zIndex": 900, "position": "relative"}, children=[
        html.Div(style={"position": "fixed", "top": 66, "right": 10, "width": 350}, children=[
            html.Div(id="toast_container_rules"),
            html.Div(id="toast_container_rules_sidebar"),
            html.Div(id="toast_container_token"),
            html.Div(id="toast_container_sidebar_fetch"),
            html.Div(id="toast_container_results_infer"),
            html.Div(id="toast_container_results_table"),
        ])
    ]),

    html.Div(id="header", children=[
        html.Div(className="col-xl-8 col-12", children=[
            html.H4("Knowledge Graph Inference Rules"),
            html.Span("In order to request a new rule, follow the instruction on the "),
            dcc.Link("confluence page",
                     href="https://bbpteam.epfl.ch/project/spaces/display/BBKG/Inference+and+Data+Generalization+Rules",
                     target="_blank"),
        ]),
        html.Div(className="d-flex justify-content-end col-xl-4 col-12", children=auth),
        dcc.Store(id='stored_token', storage_type='session'),
    ], className="row mt-4"),

    html.Div(className="card mt-4", children=[
        html.Button(className="dropdown-toggle", style={"border": "none"},
                    **{"data-bs-toggle": "collapse", "data-bs-target": "#collapse_rule"}),
        html.Div(className="card-body", id="collapse_rule", children=html.Div([
            html.Div(className="col-xl-3 col-md-4 col-12", children=[

                html.H5(children="Search Data Generalization Rules:",
                        style={"textAlign": "center"}),
                dcc.Loading(id="sidebar_fetching_loader",
                            children=[html.Div(id="sidebar_fetching_loader_output")],
                            type="circle"),
                dcc.Loading(id="sidebar_building_loader",
                            children=[html.Div(id="sidebar_building_loader_output")],
                            type="circle"),
                to_be_filled("sidebar"),
                dcc.Store(id='sidebar_content'),
                dcc.Store(id="stored_filters")
            ]),

            html.Div(className="col-xl-5 col-md-8 col-12", children=[
                html.H5(children="Rule Search Results", style={"textAlign": "center"}),
                dcc.Loading(id="rule_fetching_loader",
                            children=[html.Div(id="rule_fetching_loader_output")],
                            type="circle"),
                to_be_filled("rule_list"),
                dcc.Store(id='stored_rules')
            ]
                     ),

            html.Div(className="col-xl-4 col-12", children=[
                html.H5(children="Selected Rule", id="selected_rule_title",
                        style={"textAlign": "center"}),
                dcc.Loading(id="selected_rule_loader",
                            children=[html.Div(id="selected_rule_loader_output")], type="circle"),
                to_be_filled("selected_rule_view"),
                dcc.Store(id='selected_rule')

            ]),

        ], className="row"))
    ]),

    html.Div(className="card mt-4", children=[
        html.Button(className="dropdown-toggle", style={"border": "none"},
                    **{"data-bs-toggle": "collapse", "data-bs-target": "#collapse_result"}),
        html.Div(className="card-body", id="collapse_result", children=html.Div([
            html.Div(children=[
                html.Div(className="col-xl-8 col-12", children=[
                    html.H5(children="Inference Results", style={"textAlign": "center"}),
                    dcc.Loading(id="result_fetching_loader",
                                children=[html.Div(id="result_fetching_loader_output")],
                                type="circle"),
                    dcc.Loading(id="result_displaying_loader",
                                children=[html.Div(id="result_displaying_loader_output")],
                                type="circle"),
                    to_be_filled("result_list"),
                    dcc.Store(id="stored_results")
                ]),

                html.Div(className="col-xl-4 col-12", children=[
                    html.H5(children="Selected Result",
                            id="selected_result_title", style={"textAlign": "center"}),
                    dcc.Loading(id="selected_result_loader",
                                children=[html.Div(id="selected_result_loader_output")],
                                type="circle"),
                    to_be_filled("selected_result_view"),
                    dcc.Store(id="selected_result")
                ]),
            ], className="row"),
        ]))

    ]),

], className="container-fluid")

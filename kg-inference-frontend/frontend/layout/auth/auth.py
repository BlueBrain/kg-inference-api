from dash import html, dcc

auth = html.Div(style={"width": "25%", "minWidth": "400px"}, children=[
    html.Button(className="btn btn-light card-header dropdown-toggle", type="button",
                **{"data-bs-toggle": "collapse", "data-bs-target": "#collapse_auth"},
                children="Authenticate", style={"textAlign": "right"}),

    html.Div(className="collapse", id="collapse_auth", children=[
        html.Div(className="card-body", children=[
            html.Div(className="d-flex justify-content-end",
                     style={"marginLeft": "auto", "marginRight": 0}, children=[
                dcc.Loading(
                    id="auth-loading",
                    children=[html.Div([html.Div(id="token_header_alert")])],
                    type="circle",
                ),
                dcc.Input(id="token_input", name="token_input", className="form-control",
                          placeholder="Authentication token", style={"width": "50%"}),

                html.Button(children="Save", id="save_token_button", className="btn btn-dark"),

            ])
        ])
    ])
], className="card")

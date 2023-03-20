from dash import dcc, html
import plotly.graph_objects as go
from itertools import product
from layout.rule.inference_inputs import get_input_group
from data.utils import enforce_list
from data.result.result import Attribute
from data.result.result_resource import ResultResource

DEFAULT_X_AXIS, DEFAULT_Y_AXIS = Attribute.BRAIN_REGION.value, Attribute.TYPE.value

dropdown_key_title_map = {
    Attribute.BRAIN_REGION.value: "Brain Regions",
    Attribute.TYPE.value: "Data Types",
    Attribute.E_TYPE.value: "E Types",
    Attribute.M_TYPE.value: "M Types",
    Attribute.CONTRIBUTION_LABEL.value: "Contributors"
}


def build_result_chart_with_controls(results):
    return html.Div(children=[
        html.Div(className="row", children=[

            get_input_group(
                form_control=dcc.Dropdown(id="x_axis_chart", options=dropdown_key_title_map,
                                          value=DEFAULT_X_AXIS),
                label="X Axis"
            ),
            get_input_group(
                form_control=dcc.Dropdown(id="y_axis_chart", options=dropdown_key_title_map,
                                          value=DEFAULT_Y_AXIS),
                label="Y Axis"
            ),
            html.Div(className="col-2 mt-2", children=[
                html.Button(id="chart_button", children="Change axis", className="btn btn-dark mt-4")
            ])
        ]),
        html.Div(id="chart_container", children=build_result_chart(results))
    ])


def build_result_chart(data: list, x_axis=DEFAULT_X_AXIS, y_axis=DEFAULT_Y_AXIS):
    data = [ResultResource.store_to_class(e) for e in data]
    x_unflattened = [enforce_list(el.get_attribute(Attribute(x_axis), to_str=False)) for el in data]
    y_unflattened = [enforce_list(el.get_attribute(Attribute(y_axis), to_str=False)) for el in data]

    x = list(set([item for el in x_unflattened for item in el]))
    y = list(set([item for el in y_unflattened for item in el]))

    def make_div(axis):
        return html.H6(f"Could not find {dropdown_key_title_map[axis]} in the results",
                       style={"textAlign": "center"}, className="mt-4")

    if len(x) == 1 and x[0] is None:
        return make_div(x_axis)

    if len(y) == 1 and y[0] is None:
        return make_div(y_axis)

    z = [[0] * len(x) for _ in range(len(y))]

    for i in range(len(x_unflattened)):
        for (x_item, y_item) in product(x_unflattened[i], y_unflattened[i]):
            z[y.index(y_item)][x.index(x_item)] += 1

    layout = go.Layout(
        title="Heatmap", height=550, autosize=True,
        xaxis=go.layout.XAxis(title=dropdown_key_title_map[x_axis], linecolor="black", linewidth=1, automargin=True),
        yaxis=go.layout.YAxis(title=dropdown_key_title_map[y_axis], linecolor="black", linewidth=1, automargin=True),
    )

    heatmap = go.Figure(data=go.Heatmap(x=x, y=y, z=z), layout=layout)
    heatmap.update_traces(colorbar={"dtick": 1}, selector={"type": 'heatmap'})
    return dcc.Graph(figure=heatmap)

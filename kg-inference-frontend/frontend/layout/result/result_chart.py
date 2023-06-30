from typing import List
from collections import defaultdict
from itertools import product

from dash.development.base_component import Component
from dash import dcc, html
import plotly.graph_objects as go

from data.rule import Rule
from data.utils import enforce_list, get_model_label
from data.result.result import Attribute
from data.result.result_resource import ResultResource

from layout.rule.inference_inputs import get_input_group


DEFAULT_X_AXIS, DEFAULT_Y_AXIS = Attribute.BRAIN_REGION.value, Attribute.TYPE.value

dropdown_key_title_map = dict(
    (att.value, f"{att.value}s")
    for att in [
        Attribute.BRAIN_REGION,
        Attribute.TYPE,
        Attribute.E_TYPE,
        Attribute.M_TYPE,
        Attribute.CONTRIBUTION_LABEL
    ]
)


def build_result_chart_with_controls(results: List[ResultResource], rule: Rule):
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
                html.Button(id="chart_button", children="Change axis",
                            className="btn btn-dark mt-4")
            ])
        ]),
        html.Div(id="chart_container", children=build_result_chart(results)),
        html.Div(id="chart_score_container", children=build_score_chart(results, rule))
    ])


def build_result_chart(data: List[ResultResource], x_axis=DEFAULT_X_AXIS, y_axis=DEFAULT_Y_AXIS) \
        -> Component:
    if len(data) == 0:
        return html.H5(children="No Results")

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
        xaxis=go.layout.XAxis(title=dropdown_key_title_map[x_axis], linecolor="black",
                              linewidth=1, automargin=True),
        yaxis=go.layout.YAxis(title=dropdown_key_title_map[y_axis], linecolor="black",
                              linewidth=1, automargin=True),
    )

    heatmap = go.Figure(data=go.Heatmap(x=x, y=y, z=z), layout=layout)
    heatmap.update_traces(colorbar={"dtick": 1}, selector={"type": "heatmap"})
    return dcc.Graph(figure=heatmap)


def build_score_chart(data: List[ResultResource], rule: Rule) -> Component:
    combined_score = [e.get_attribute(Attribute.SCORE) for e in data]

    if all(e is None for e in combined_score):
        return html.Div()

    score_breakdown_attribute = [e.get_attribute(Attribute.SCORE_BREAKDOWN)[0] for e in data]

    to_graph = lambda x, title: dcc.Graph(figure=go.Figure(
        data=go.Histogram(x=x),
        layout=go.Layout(title=title))
    )
    score_breakdown = defaultdict(list)

    for entry in score_breakdown_attribute:
        for key, value in entry.items():
            score, weight = value
            title = f"{get_model_label(key, rule=rule)}, weight={weight}"
            score_breakdown[title].append(score)

    data = [to_graph(x=values, title=title) for title, values in score_breakdown.items()] + \
           [to_graph(x=combined_score, title="Combined Score")]

    return html.Div(children=data)

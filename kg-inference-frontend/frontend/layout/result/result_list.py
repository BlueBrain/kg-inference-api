from dash import dcc
from layout.result.result_table import build_result_table
from layout.result.result_chart import build_result_chart_with_controls


def build_result_list(results):
    return dcc.Tabs(children=[
        dcc.Tab(label="Table View", children=build_result_table(results)),
        dcc.Tab(label="Chart View", children=build_result_chart_with_controls(results))
    ])

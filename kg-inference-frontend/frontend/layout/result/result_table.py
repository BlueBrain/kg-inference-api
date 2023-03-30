from dash import dash_table, html, dcc
from data.result.result import Attribute
from data.result.result_resource import ResultResource
# import json


def build_result_table(results):
    if len(results) == 0:
        return html.H5(children="No Results")

    ignore_keys = [Attribute.CONTENT_URL, Attribute.AT_LOCATION, Attribute.BRAIN_REGION_ID,
                   Attribute.LINK, Attribute.M_TYPE, Attribute.E_TYPE, Attribute.CONTRIBUTION, Attribute.SUBJECT_ID,
                   Attribute.IMAGE, Attribute.ORG, Attribute.PROJECT, Attribute.DISTRIBUTION,
                   Attribute.IMAGE_STIMULUS_TYPE_LABEL]

    data = [ResultResource.store_to_class(elastic_json).get_attributes(ignore_keys=ignore_keys)
            for elastic_json in results]

    columns = [{"name": key.value, "id": key.value, "hideable": "last"} for key in list(Attribute)
               if key not in ignore_keys]

    # return html.Div([dcc.Textarea(
    #     id='textarea1',
    #     value=json.dumps(data),
    # ), dcc.Textarea(
    #     id='textarea2',
    #     value=json.dumps(columns),
    # )])

    return dash_table.DataTable(
        id="datatable_results",
        columns=columns,
        data=data,
        cell_selectable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        hidden_columns=["id"],
        row_selectable="single",
        row_deletable=True,
        page_size=15,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'fontSize': 15, 'font-family': 'sans-serif'},
        css=[
            {"selector": "p", "rule": "margin: 0"}
        ],
        export_format='xlsx',
        export_headers='display'
    )

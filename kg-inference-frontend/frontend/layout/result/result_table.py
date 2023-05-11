from typing import Dict, List

from dash import dash_table, html, dcc
from data.result.result import Attribute
from data.result.result_resource import ResultResource


def build_result_table(results, table_id, include_score: bool, rule=None):
    if len(results) == 0:
        return html.H5(children="No Results")

    ignore_keys = [Attribute.CONTENT_URL, Attribute.AT_LOCATION, Attribute.BRAIN_REGION_ID,
                   Attribute.LINK, Attribute.M_TYPE, Attribute.E_TYPE, Attribute.CONTRIBUTION,
                   Attribute.IMAGE, Attribute.ORG, Attribute.PROJECT, Attribute.DISTRIBUTION,
                   Attribute.IMAGE_STIMULUS_TYPE_LABEL, Attribute.SUBJECT_ID, Attribute.SCORE,
                   Attribute.SCORE_BREAKDOWN]

    data = [ResultResource.store_to_class(elastic_json) for elastic_json in results]

    def get_model_label(model_id):
        ips = rule["inputParameters"]
        ip = next(ip for ip in ips if ip["name"] == "IgnoreModelsParameter")["values"]
        label = next(key for key, value in ip.items() if value == model_id)
        return label.replace("_", " ")

    def format_data_point(r: ResultResource, is_with_score: bool) -> Dict:
        data_base = r.get_attributes(ignore_keys=ignore_keys)

        if not is_with_score:
            return data_base

        data_base["Combined Score"] = r.get_attribute(Attribute.SCORE)

        breakdown = r.get_attribute(Attribute.SCORE_BREAKDOWN)[0]

        for key, value in breakdown.items():
            score, weight = value
            model_label = get_model_label(key)
            data_base[f"Score for {model_label}"] = score
            data_base[f"Weight for {model_label}"] = weight

        return data_base

    def get_columns(is_with_score: bool, data_as_resource: List[ResultResource]):

        columns_base = [
            {"name": key.value, "id": key.value, "hideable": "last"}
            for key in list(Attribute)
            if key not in ignore_keys
        ]

        if not is_with_score:
            return columns_base

        added = ["Combined Score"]
        breakdown = data_as_resource[0].get_attribute(Attribute.SCORE_BREAKDOWN)[0]
        for el in breakdown.keys():
            model_label = get_model_label(el)
            added.append(f"Score for {model_label}")
            added.append(f"Weight for {model_label}")

        columns_base += [{"name": v, "id": v, "hideable": "last"} for v in added]
        return columns_base

    # include score as True for the result table, and False for the neuron morphology table
    sample_breakdown = data[0].get_attribute(Attribute.SCORE_BREAKDOWN)
    iws = include_score and sample_breakdown is not None
    columns = get_columns(is_with_score=iws, data_as_resource=data)
    data = [format_data_point(el, is_with_score=iws) for el in data]

    return dash_table.DataTable(
        id=table_id,
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
        style_header={"whiteSpace": "normal"},
        style_cell={'textAlign': 'left', 'fontSize': 15, 'font-family': 'sans-serif'},
        css=[
            {"selector": "p", "rule": "margin: 0"}
        ],
        export_format='xlsx',
        export_headers='display'
    )

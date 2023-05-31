from typing import List, Dict, Optional, Tuple

from dash import dcc
from dash.development.base_component import Component

from data.result.result_resource import ResultResource
from layout.result.result_plot import build_result_plot_with_controls
from layout.result.result_table import build_result_table
from layout.result.result_chart import build_result_chart_with_controls
from query.forge import NM_RULE_IDS


def build_result_list(results: Dict[str, Dict], rule: Dict, token: str,
                      selected_nm: Optional[ResultResource]) -> \
        Tuple[Optional[Dict], Component]:

    data: Dict[str, ResultResource] = dict(
        (id_, ResultResource.store_to_class(e))
        for id_, e in results.items()
    )
    results_list: List[ResultResource] = list(data.values())

    children = [
        dcc.Tab(
            label="Table View",
            children=build_result_table(
                results=results_list,
                table_id="datatable_results", include_score=True, rule=rule
            )
        ),
        dcc.Tab(
            label="Chart View",
            children=build_result_chart_with_controls(
                results=results_list
            )
        )
    ]

    if rule["id"] in NM_RULE_IDS:

        prepared_plot_data, plot_container = build_result_plot_with_controls(
            results=data,
            rule=rule,
            token=token,
            selected_nm=selected_nm,
        )

        children.append(
            dcc.Tab(
                label="Plot View",
                children=plot_container
            )
        )
    else:
        prepared_plot_data = None

    return prepared_plot_data, dcc.Tabs(children=children)

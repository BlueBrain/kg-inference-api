from dash import dash_table


def build_rule_table(stored_rules):
    table_visible_keys = ["name", "description", "resourceType"]
    table_labels = ["Name", "Description", "Result Type"]

    keys = table_visible_keys + ["id"]
    rules_table_format = [dict(zip(keys, list(map(rule.get, keys))))
                          for rule in stored_rules]

    return dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={'textAlign': 'left', 'fontSize': 15, 'font-family': 'sans-serif'},
        id="datatable_rules",
        data=rules_table_format,
        columns=[{"name": label, "id": key} for (label, key) in zip(table_labels, table_visible_keys)],
        row_selectable="single",
        cell_selectable=False,
        page_size=5,
        style_table={'overflowX': 'auto'},
    )

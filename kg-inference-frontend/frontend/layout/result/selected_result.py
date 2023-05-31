from dash import html, dcc
from layout.result.custom_results.trace_view import trace_images
from layout.result.custom_results.neuron_morphology_view import neuron_morphology_3d
from data.result.result import Attribute
from data.result.result_resource import ResultResource
from data.result.distribution import Distribution


def build_selected_result(result, token, app):
    result_resource = ResultResource.store_to_class(result)

    ignore_keys = [Attribute.CONTRIBUTION, Attribute.BRAIN_REGION_ID,
                   Attribute.ENCODING_FORMAT, Attribute.CONTENT_URL, Attribute.AT_LOCATION,
                   Attribute.LINK, Attribute.IMAGE, Attribute.ORG, Attribute.PROJECT,
                   Attribute.DISTRIBUTION, Attribute.IMAGE_STIMULUS_TYPE_LABEL,
                   Attribute.SCORE_BREAKDOWN]

    attributes = result_resource.get_attributes(ignore_keys=ignore_keys)

    metadata = [
        html.Div(children=[
            html.Label(children=f"{key}:", htmlFor=key,
                       style={"marginRight": "5px", "fontWeight": "bold"}),
            html.Span(children=value_content, id=key)
        ], className="form-group mt-4")

        for key, value_content in attributes.items()
    ]

    def one_distribution(i, distribution: Distribution):

        return html.Div(children=[
            html.H6(f"Distribution {i}", className="mt-4"),
            html.Div(
                children=[
                    html.Div(children=[
                        html.Label(children=f"{label}:", htmlFor=f"{label}_{i}",
                                   style={"marginRight": "5px", "fontWeight": "bold"}),
                        html.Span(children=value, id=f"{label}_{i}")
                    ])
                    for label, value in zip([Attribute.ENCODING_FORMAT.value,
                                             Attribute.CONTENT_URL.value,
                                             Attribute.AT_LOCATION.value],
                                            [distribution.encoding_format,
                                             distribution.content_url,
                                             distribution.at_location])
                ]
            )
        ])

    distributions = result_resource.get_attribute(Attribute.DISTRIBUTION)

    distribution_content = html.Div(children=[
        html.H5(className="mt-4", children="Distributions"),
        html.Div(children=[one_distribution(i + 1, d) for i, d in enumerate(distributions)])
    ])

    metadata.append(distribution_content)

    name = result_resource.get_attribute(Attribute.NAME)
    link = result_resource.get_attribute(Attribute.LINK)

    title = [
        html.H5(className="me-2", children=name if name else "Selected Result"),
        dcc.Link(children=html.Img(src=app.get_asset_url('nexus_logo.png'),
                                   style={"height": "25px"}), href=link, target="_blank")
        if link else html.Div()
    ]

    result_type = result_resource.get_attribute(Attribute.TYPE, to_str=False)
    images = result_resource.get_attribute(Attribute.IMAGE)

    if result_type and "NeuronMorphology" in result_type and len(distributions) > 0:
        assets = neuron_morphology_3d(result_resource, distributions, token)
        tab_title = "3D View"
    elif result_type and "Trace" in result_type and images and len(images) > 0:
        assets = trace_images(result_resource, images, token)
        tab_title = "Images"
    else:
        assets = []
        tab_title = "Assets"

    content = dcc.Tabs(children=[
        dcc.Tab(label="Metadata", children=metadata),
        dcc.Tab(label=tab_title, children=assets, disabled=len(assets) == 0)
    ])

    return content, title

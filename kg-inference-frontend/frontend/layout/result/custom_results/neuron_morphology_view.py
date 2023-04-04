from dash import dcc
import os
import shutil
import neurom as nm
from neurom.view.plotly_impl import get_figure
from data.result.distribution import Distribution
from query.forge import download_from_content_url
from data.result.attribute import Attribute
from datetime import datetime


def neuron_morphology_3d(result, distributions: [Distribution], token):
    path = f"./{datetime.now().strftime('%m-%d-%Y.%H:%M:%S')}"
    filename = "nm.swc"
    os.makedirs(path, exist_ok=True)
    path_to_download = os.path.join(path, filename)

    for el in distributions:
        if "swc" in el.encoding_format:
            download_from_content_url(content_url=el.content_url, content_type=el.encoding_format,
                                      org=result.get_attribute(Attribute.ORG),
                                      project=result.get_attribute(Attribute.PROJECT),
                                      path_to_download=path_to_download, token=token)

            m = nm.load_morphology(path_to_download)
            fig = get_figure(m, plane='3d', title="3D View")
            graph = dcc.Graph(id=f'neurom', figure=fig)
            shutil.rmtree(path)
            return [graph]

    return []

from query.forge import forge_get_files
from itertools import groupby
from dash import html, dcc
from data.result.attribute import Attribute
import base64


def trace_images(result_resource, images, token):
    file_binaries = forge_get_files(
        file_ids=[image.id for image in images],
        token=token,
        org=result_resource.get_attribute(Attribute.ORG),
        project=result_resource.get_attribute(Attribute.PROJECT)
    )

    images = [{
        "id": image.id,
        "label": image.stimulus_type.label,
        "repetition": image.repetition,
        "binary": file_binaries[i],
        "about": image.about
    } for i, image in enumerate(images)]

    def group(values, key):
        def acc(x):
            return x[key]
        return dict((k, list(g)) for k, g in groupby(sorted(values, key=acc), key=acc))

    images_grouped_stimuli_label = group(images, "label")

    images_grouped_repetition = dict((key, group(image_list, "repetition"))
                                     for key, image_list in images_grouped_stimuli_label.items())

    def one_stimulus(stimuli_repetition_group):
        def image_thing(image):
            content = image["binary"]
            test = base64.b64encode(content).decode("utf-8")
            return html.Img(className="img-fluid", src="data:image/png;base64, " + test)

        def tab_content(repetition_group):
            return html.Div(className="container", children=html.Div([
                html.Div(className="col-6", children=image_thing(image))
                for image in repetition_group
            ], className="row"))

        def tabify(stimuli_group):
            return [
                dcc.Tab(label=f"Repetition {repetition_number}", children=tab_content(repetition_group))
                for repetition_number, repetition_group in stimuli_group.items()
            ]

        return dcc.Tabs(children=tabify(stimuli_repetition_group))

    all_stimuli = dict((key, one_stimulus(list_images))
                       for key, list_images in images_grouped_repetition.items())

    return dcc.Tabs(children=[dcc.Tab(label=key, children=stimulus)
                              for key, stimulus in all_stimuli.items()])

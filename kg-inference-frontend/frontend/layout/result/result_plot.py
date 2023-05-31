import io
from typing import List, Dict, Tuple, Optional

from data.result.attribute import Attribute
from dash.development.base_component import Component
from data.result.result_resource import ResultResource
from data.utils import get_model_label
from layout.rule.inference_inputs import get_input_group
from query.forge import get_embedding_vectors, ForgeError
from dash import html, dcc
from sklearn.manifold import TSNE
from plotly.express import scatter
from pandas import DataFrame, read_pickle
import numpy as np
import os
import zipfile

DEFAULT_PERPLEXITY = 5
DEFAULT_ITERATIONS = 1000
DEFAULT_LABEL = Attribute.BRAIN_REGION
LOAD_DATA = True

RANGE_PERPLEXITY = range(5, 100, 5)
RANGE_ITERATIONS = [1000 * (i + 1) for i in range(10)]
VALID_LEGEND_KEYS = [Attribute.BRAIN_REGION, Attribute.M_TYPE]
TSNE_SUBDIRECTORY = "tsne"

DataFormat = Dict[str, Tuple[str, Dict]]

FILENAMES = {
    "https://bbp.epfl.ch/neurosciencegraph/data/7479d675-0fe4-4a04-898c-94f482c2bd30":
        "SEU_morph_axon_coproj_node2vec_cosine",
    "https://bbp.epfl.ch/neurosciencegraph/data/0da5d33e-798d-4169-bfbe-4f38f9be8993":
        "SEU_morph_brain_region_poincare_bbp",
    "https://bbp.epfl.ch/neurosciencegraph/data/04982fcd-472c-4512-8033-873897de5ce5":
        "SEU_morph_coordinates_euclidean",
    "https://bbp.epfl.ch/neurosciencegraph/data/7c99b41a-7f24-4e67-923c-87cd99d05be1":
        "SEU_morph_dendrite_coproj_node2vec_cosine",
    "https://bbp.epfl.ch/neurosciencegraph/data/462c62c8-d4be-48e5-bda4-353d57d616bf":
        "SEU_morph_neurite_features_euclidean",
    "https://bbp.epfl.ch/neurosciencegraph/data/5484fc15-1cde-4deb-b8e7-01c6771c13a4":
        "SEU_morph_TMD_euclidean"
}


class TSNEException(Exception):

    def __init__(self, count):
        self.message = f"TSNE perplexity = {DEFAULT_PERPLEXITY}, " \
                       f"result set + reference size: {count}"

        super().__init__(self.message)


def _build_controls(load: bool, label: Attribute, perplexity: int, nb_iterations: int) \
        -> Component:
    controls = [
        get_input_group(
            form_control=dcc.RadioItems(
                options=[e.value for e in VALID_LEGEND_KEYS],
                inline=True,
                value=label.value,
                id="plot_legend_picker",
                className="form-control",
                labelStyle={"paddingRight": "10px"}
            ),
            label="Plot label"
        )
    ]

    if load:
        def to_marks(list_values):
            return dict(zip(list_values, [str(e) for e in list_values]))

        controls.extend([

            get_input_group(
                form_control=dcc.Slider(
                    marks=to_marks(RANGE_ITERATIONS),
                    id="iteration_slider",
                    value=nb_iterations,
                    step=None
                ),
                label="TSNE Number of iterations"
            ),
            get_input_group(
                form_control=dcc.Slider(
                    marks=to_marks(RANGE_PERPLEXITY),
                    id="perplexity_slider",
                    value=perplexity,
                    step=None
                ),
                label="TSNE Perplexity"
            )

        ])
    return html.Div(controls)


def build_result_plot_with_controls(results: Dict[str, ResultResource], rule: Dict,
                                    token: str, selected_nm: ResultResource) -> \
        Tuple[Optional[DataFormat], Component]:

    if len(results) == 0:
        return None, html.H5(children="No Results")

    try:
        prepared_plot_data: DataFormat = prepare_data(
            results, rule, token, selected_nm,
            load=LOAD_DATA,
            perplexity=DEFAULT_PERPLEXITY,
            nb_iterations=DEFAULT_ITERATIONS
        )
    except (ForgeError, TSNEException) as e:
        return None, html.Div(e.message)

    plot_div = html.Div(children=[
        _build_controls(
            load=LOAD_DATA,
            perplexity=DEFAULT_PERPLEXITY,
            nb_iterations=DEFAULT_ITERATIONS,
            label=DEFAULT_LABEL
        ),
        html.Div(
            id="plot_container",
            children=build_result_plot(
                prepared_data=prepared_plot_data,
                legend_field_name=DEFAULT_LABEL
            )
        )
    ])

    return prepared_plot_data, plot_div


def build_result_plot(prepared_data: DataFormat,
                      legend_field_name: Attribute):
    return [
        dcc.Graph(
            figure=scatter(
                data_frame=DataFrame.from_dict(dataframe_dict),
                x="x",
                y="y",
                size="size",
                color=legend_field_name.value,
                custom_data="id",
                hover_name="labels",
                hover_data={
                    "x": False,
                    "y": False,
                    "score": True,
                    "size": False
                },
                title=title
            ),
            id={
                "name": model_id,
                "index": "embedding_graph",
            }
        )
        for model_id, (title, dataframe_dict) in prepared_data.items()
    ]


def _prepare_data_load(
        model_id: str,
        entity_ids: List[str],
        token: str,
        results: Dict[str, ResultResource],
        selected_nm: ResultResource,
        scores: Dict[str, Dict],
        perplexity: int,
        nb_iterations: int
) -> Dict:
    """
    For a list of inference results similar to the input selected_nm, according to a model:

    - Loads a zip file containing multiple runs of 2D reduction of embeddings,
    for different hyperparameters. Each file in the zip file is a pickle file that
    holds a single dataframe corresponding to the TSNE result for a perplexity/number of
    iterations pair. This dataframe holds the following columns:
        - the point 2D coordinates
        - the point tooltip label (UUID and rev of the derived entity)
        - the derived entity id
    - Adds additional features that are necessary for plotting:
            - the point size (the starting point has a bigger size)
            - the embedding similarity score
            - a set of columns that are valid point labels (color): these are attributes of the
            derived entity id, and the point color is attributed based on the value of this
            attribute
    - Returns this dataframe
    """
    tsne_sub_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "../../assets/",
                                 TSNE_SUBDIRECTORY, FILENAMES[model_id])

    archive = zipfile.ZipFile(f"{tsne_sub_path}.zip", "r")
    pickle_data = archive.read(f"{perplexity}_{nb_iterations}.pickle")
    dataframe = read_pickle(io.BytesIO(pickle_data))
    dataframe = dataframe.loc[entity_ids]
    embedding_entity_ids = dataframe["id"]
    embedding_entities = [results[id_] for id_ in embedding_entity_ids]

    size = [
        40 if e == selected_nm.get_attribute(Attribute.ID) else 10
        for e in embedding_entity_ids
    ]
    dataframe["size"] = size

    embedding_scores = [
        scores[id_][model_id][0] if id_ in scores else "No score"
        for id_ in embedding_entity_ids
    ]
    dataframe["score"] = embedding_scores

    for legend_type_i in VALID_LEGEND_KEYS:
        values = [e.get_attribute(legend_type_i) for e in embedding_entities]
        values = [(value if value else "No value") for value in values]
        dataframe[legend_type_i.value] = values

    return dataframe.to_dict()


def _prepare_data_build(
        model_id: str,
        entity_ids: List[str],
        token: str,
        results: Dict[str, ResultResource],
        selected_nm: ResultResource,
        scores: Dict[str, Dict],
        perplexity: int,
        nb_iterations: int
) -> Dict:
    """
        For a list of inference results similar to the input selected_nm, and for a single model:
        - Retrieves the embeddings for these results
        - Reduces them to 2D, only for the default parameters of TSNE
        - Organises them into a dataframe holding the
            - the point 2D coordinates
            - the point tooltip label (UUID and rev of the derived entity)
            - the derived entity id

            - the point size (the starting point has a bigger size)
            - the embedding similarity score
            - a set of columns that are valid point labels (color): these are attributes of the
            derived entity id, and the point color is attributed based on the value of this
            attribute
        - Returns this dataframe
        """

    count = len(results) + 1

    if count <= DEFAULT_PERPLEXITY:
        raise TSNEException(count)

    embeddings_json: List[Dict] = get_embedding_vectors(
        entity_ids=entity_ids, model_id=model_id, token=token
    )

    embeddings_info = [
        (
            e["derivation"]["entity"]["id"],
            e["name"],
            e["embedding"]
        )
        for e in embeddings_json
    ]

    embedding_entity_ids, labels, node_embeddings = zip(*embeddings_info)
    embedding_vectors = np.array(list(node_embeddings))
    embedding_entities = [results[id_] for id_ in embedding_entity_ids]

    embedding_scores = [
        scores[id_][model_id][0] if id_ in scores else "No score"
        for id_ in embedding_entity_ids
    ]

    two_d_vectors = TSNE(n_components=2, perplexity=perplexity, n_iter=nb_iterations) \
        .fit_transform(embedding_vectors)

    x, y = two_d_vectors[:, 0], two_d_vectors[:, 1]

    size = [
        40 if e == selected_nm.get_attribute(Attribute.ID) else 10
        for e in embedding_entity_ids
    ]

    dataframe = DataFrame(
        data={
            "x": x,
            "y": y,
            "labels": labels,
            "id": embedding_entity_ids,

            "size": size,
            "score": embedding_scores
        },
        index=embedding_entity_ids
    )

    for legend_type_i in VALID_LEGEND_KEYS:
        values = [e.get_attribute(legend_type_i) for e in embedding_entities]
        values = [(value if value else "No value") for value in values]
        dataframe[legend_type_i.value] = values

    return dataframe.to_dict()


def prepare_data(results: Dict[str, ResultResource], rule: Dict, token: str,
                 selected_nm: ResultResource, load: bool,
                 perplexity: int, nb_iterations: int) \
        -> DataFormat:
    """
    Organises these dataframe into a dictionary, with key the model_id,
    and value a tuple of the model label and the dataframe
    """

    prepare_data_fc = _prepare_data_load if load else _prepare_data_build

    scores: Dict[str, Dict] = dict(
        (e.get_attribute(Attribute.ID), e.get_attribute(Attribute.SCORE_BREAKDOWN)[0])
        for e in results.values()
    )

    results.update({selected_nm.get_attribute(Attribute.ID): selected_nm})
    entity_ids = [e.get_attribute(Attribute.ID) for e in results.values()]

    model_list: List[str] = list(scores[entity_ids[0]].keys())
    # TODO maybe get this from UI state instead of results

    data_formatted = dict(
        (
            model_id,
            (
                f"{get_model_label(model_id, rule)}, "
                f"TSNE perplexity: {perplexity}, "
                f"nb iterations: {nb_iterations}",
                prepare_data_fc(
                    model_id=model_id,
                    entity_ids=entity_ids,
                    token=token,
                    scores=scores,
                    selected_nm=selected_nm,
                    results=results,
                    perplexity=perplexity,
                    nb_iterations=nb_iterations,
                )
            )
        )
        for model_id in model_list
    )

    return data_formatted

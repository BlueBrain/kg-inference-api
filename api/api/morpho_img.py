"""
Module: morpho_imh.py

This module provides functions to generate morphology PNG images.
"""

import io
from typing import Union
from urllib.parse import urlparse
import requests
import neurom as nm
import matplotlib.pyplot as plt
from fastapi import Header, Response
from neurom.view import matplotlib_impl, matplotlib_utils
from api.exceptions import InvalidUrlParameterException, ResourceNotFoundException


def get_morphology_file_content(authorization: str = "", content_url: str = "") -> str:
    """
    Gets the File content of an SWC distribution (by requesting the resource from its content_url).

    Parameters:
        - authorization (str): Authorization header containing the access token.
        - content_url (str): URL of the SWC distribution.

    Returns:
        str: File content as a string.

    Raises:
        str: Error message if the request to the content_url fails.
    """
    parsed_content_url = urlparse(content_url)

    if not all([parsed_content_url.scheme, parsed_content_url.netloc, parsed_content_url.path]):
        raise InvalidUrlParameterException

    response = requests.get(content_url, headers={"authorization": authorization}, timeout=15)

    if response.status_code == 200:
        file_content = response.content.decode("utf-8")
        return file_content
    if response.status_code == 404:
        raise ResourceNotFoundException
    raise requests.exceptions.RequestException


def read_image(authorization: str = Header(None), content_url: str = "", dpi: Union[int, None] = 72) -> Response:
    """
    Returns a PNG image of a morphology (by generating a matplotlib figure from its SWC distribution).

    Parameters:
        - authorization (str): Authorization header containing the access token.
        - content_url (str): URL of the SWC distribution.

    Returns:
        Response: FastAPI Response object containing the PNG image.
    """

    morph = get_morphology_file_content(authorization, content_url)

    nrn = nm.load_morphology(io.StringIO(morph), reader="swc")
    fig, ax = matplotlib_utils.get_figure()

    matplotlib_impl.plot_morph(nrn, ax)

    ax.set_title("")
    ax.set_aspect("equal")
    ax.set_frame_on(False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    bounds = ax.dataLim.bounds
    white_space = 0.05
    ax.set_xlim(bounds[0] - white_space, bounds[0] + bounds[2] + white_space)
    ax.set_ylim(bounds[1] - white_space, bounds[1] + bounds[3] + white_space)

    fig.set_tight_layout(True)

    buffer = io.BytesIO()

    fig.savefig(buffer, dpi=dpi, format="png")

    buffer.seek(0)

    plt.close()

    return Response(buffer.getvalue(), media_type="image/png")

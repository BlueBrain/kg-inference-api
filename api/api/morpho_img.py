import requests
import neurom as nm
import matplotlib.pyplot as plt
import io
from api.exceptions import ResourceNotFoundException

from fastapi import Header, Response
from neurom.view import matplotlib_impl, matplotlib_utils


def get_morphology_file_content(authorization: str = "", content_url: str = ""):
    """
    Gets the File content of an SWC distibution (by requesting the resource from its content_url).
    """

    response = requests.get(content_url, headers={"authorization": authorization})

    if response.status_code == 200:
        file_content = response.content.decode("utf-8")

        return file_content

    elif response.status_code == 404:
        raise ResourceNotFoundException

    else:
        raise requests.exceptions.RequestException


def read_image(authorization: str = Header(None), content_url: str = ""):
    """
    Returns a PNG imgage of a morphology (by generating a matplotlib figure from a its SWC distribution).
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

    fig.savefig(buffer, dpi=72, format="png")

    buffer.seek(0)

    plt.close()

    return Response(buffer.getvalue(), media_type="image/png")

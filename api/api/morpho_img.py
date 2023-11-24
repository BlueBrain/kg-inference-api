import requests
import neurom as nm
import matplotlib.pyplot as plt
import io
import hashlib

from fastapi import Header
from fastapi.responses import FileResponse
from neurom.view import matplotlib_impl, matplotlib_utils


def get_morphology_file_content(authorization: str = "", content_url: str = ""):
    """
    Gets the File content of an SWC distibution (by requesting the resource from its content_url).
    """

    response = requests.get(content_url, headers={"authorization": authorization})

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)

    file_content = response.content.decode("utf-8")

    return file_content


def get_file_path(content_url: str = ""):
    """
    Creates a file path from a content_url, to be used for writing the generated PNG.
    """

    encoded_content_url = hashlib.sha1(bytes(content_url, "utf8")).hexdigest()
    file_name = f"{encoded_content_url}.png"
    file_path = f"dist/{file_name}"

    return file_path


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

    file_path = get_file_path(content_url=content_url)

    fig.savefig(file_path, dpi=72)

    plt.close()

    return FileResponse(file_path, media_type="image/png")

from typing import List, Union, Optional, Dict
from urllib.parse import quote_plus as url_encode
import os
import requests
from nexussdk.utils.http import decode_json_ordered, header_parts, header_accept
from nexussdk.files import SEGMENT


# nexussdk/files.py
def fetch(environment: str,
          token: str,
          org_label: str,
          project_label: str,
          file_id: str,
          rev: Optional[int] = None,
          tag: Optional[str] = None,
          out_filepath: Optional[str] = None) -> Dict:
    """
        Fetches a distant file and returns the metadata of this file. In addition, if the argument `out_filepath` can
        be of three forms:
        - out_filepath=None (default): the binary is not fetched
        - out_filepath="./some/folder/" the binary is fetched and written in this dir with it's original filename
        - out_filepath="./somefile.jpg" the binary is fetched and written under this exact filename
        - out_filepath="return" the binary is returned
        In case of error, an exception is thrown.
        :param token:
        :param environment:
        :param org_label: The label of the organization that the file belongs to
        :param project_label: The label of the project that the file belongs to
        :param file_id: id of the file
        :param rev: OPTIONAL fetches a specific revision of a file (default: None, fetches the last)
        :param tag: OPTIONAL fetches the file version that has a specific tag (default: None)
        :param out_filepath: OPTIONAL the filename to write (default: None)
        :return: Payload of the whole file as a dictionary, or the binary
    """

    if rev is not None and tag is not None:
        raise Exception("The arguments rev and tag are mutually exclusive. One or the other must be chosen.")

    # the elements composing the query URL need to be URL-encoded
    org_label = url_encode(org_label)
    project_label = url_encode(project_label)
    file_id = url_encode(file_id)

    path = [SEGMENT, org_label, project_label, file_id]

    response_metadata = http_get(environment=environment, path=path, rev=rev, tag=tag, token=token)
    response_binary = http_get(environment=environment, path=path, get_raw_response=True,
                               accept="all", stream=True, rev=rev, tag=tag, token=token)

    if out_filepath is not None:

        if out_filepath == "return":
            return response_binary.content

        if os.path.isdir(out_filepath):
            out_filepath = os.path.join(out_filepath, response_metadata["_filename"])

        # we write the result of the request into a file
        with open(out_filepath, "wb") as f:
            for chunk in response_binary.iter_content(chunk_size=4096):
                f.write(chunk)

    return response_metadata


# nexussdk/utils/http.py

def http_get(environment: str, token: str, path: Union[str, List[str]], stream=False, get_raw_response=False,
             use_base=False, data_type="default", accept="json", params=None, **kwargs):
    """
        Wrapper to perform a GET request.

        :param token:
        :param environment:
        :param accept:
        :param data_type:
        :param path: complete URL if use_base si False or just the ending if use_base is True
        :param params: OPTIONAL provide some URL parameters (?foo=bar&hello=world) as a dictionary
        :param use_base: OPTIONAL if True, the Nexus env provided by nexus.config.set_environment will
        be prepended to path. (default: False)
        :param get_raw_response: OPTIONAL If True, the object provided by requests.get will be directly returned as is
        (convenient when getting a binary file). If False, a dictionary representation of the response will be returned
        (default: False)
        :param stream: OPTIONAL True if GETting a file (default: False)
        :return: if get_raw_response is True, returns the request.get object. If get_raw_response is False, return the
        dictionary that is equivalent to the json response
    """
    header = prepare_header(token, data_type, accept)
    full_url = _full_url(path=path, use_base=use_base, environment=environment)
    if params:
        response = requests.get(full_url, headers=header, stream=stream, params=params, **kwargs)
    else:
        response = requests.get(full_url, headers=header, stream=stream, params=kwargs)
    response.raise_for_status()

    if get_raw_response:
        return response

    return decode_json_ordered(response.text)


# nexussdk/utils/http.py
def prepare_header(token, type="default", accept="json"):
    """
        Prepare the header of the HTTP request by fetching the tokenfrom the config
        and few other things.

        :param token:
        :param type: string. Must be one of the keys in the above declared dict header_parts
        :param accept: OPTIONAL if "json", the answer will be JSON, if "all" it will be something else if the
                       request can send something else (e.g. binary)

    """

    header = {**header_parts["common"], **header_parts[type]}

    if accept in header_accept:
        header["Accept"] = header_accept[accept]

    header["Authorization"] = "Bearer " + token
    return header


# nexussdk/utils/http.py
def _full_url(environment: str, path: Union[str, List[str]], use_base: bool) -> str:
    # 'use_base' is temporary for compatibility with previous code sections.
    if use_base:
        return environment + path

    if isinstance(path, str):
        return path
    if isinstance(path, list):
        url = [environment] + path
        return "/".join(url)

    raise TypeError("Expecting a string or a list!")
